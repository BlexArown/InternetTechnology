import time
from dataclasses import dataclass
from typing import Callable, Optional


NEW = "NEW"
PAID = "PAID"
DONE = "DONE"
CANCELLED = "CANCELLED"

FINAL_STATES = {DONE, CANCELLED}

PAY_OK = "PAY_OK"
PAY_FAIL = "PAY_FAIL"
COMPLETE = "COMPLETE"
CANCEL = "CANCEL"
RESERVE_OK = "RESERVE_OK"
RESERVE_FAIL = "RESERVE_FAIL"


_TRANSITIONS = {
    (NEW, PAY_OK): PAID,
    (NEW, PAY_FAIL): CANCELLED,

    (NEW, RESERVE_OK): NEW,         # резерв не меняет статус заказа
    (NEW, RESERVE_FAIL): CANCELLED, # если резерв не удался, то отменяем

    (PAID, COMPLETE): DONE,
    (PAID, CANCEL): CANCELLED,
}


def next_state(state: str, event: str) -> str:
    if state in FINAL_STATES:
        return state
    return _TRANSITIONS.get((state, event), state)

@dataclass
class Order:
    order_id: str
    state: str = NEW
    reserved: bool = False  # условно "зарезервирован товар"
    paid: bool = False      # условно "деньги списаны"


class SagaError(RuntimeError):
    pass

def _retry_until_success(action: Callable[[], None], *, initial_delay: float = 0.2, max_delay: float = 2.0, multiplier: float = 2.0, ) -> None:
    delay = initial_delay
    while True:
        try:
            action()
            return
        except Exception:
            time.sleep(delay)
            delay = min(max_delay, delay * multiplier)


def run_saga(order: Order, *, reserve: Callable[[Order], None], pay: Callable[[Order], None], cancel_reserve: Callable[[Order], None], complete: Optional[Callable[[Order], None]] = None,) -> Order:

    # Шаг 1: NEW уже есть
    # Шаг 2: резерв
    try:
        reserve(order)
        order.reserved = True
        order.state = next_state(order.state, RESERVE_OK)
    except Exception as e:
        # если не смогли зарезервировать - считаем это провалом бизнес-процесса
        order.state = next_state(order.state, RESERVE_FAIL)
        raise SagaError(f"Reserve failed: {e}") from e

    # Шаг 3: оплата
    try:
        pay(order)
        order.paid = True
        order.state = next_state(order.state, PAY_OK)
    except Exception as e:
        order.state = next_state(order.state, PAY_FAIL)

        if order.reserved:
            _retry_until_success(lambda: cancel_reserve(order))
            order.reserved = False

        return order

    # Шаг 4: завершение
    if complete is not None:
        complete(order)
    order.state = next_state(order.state, COMPLETE)

    return order

if __name__ == "__main__":
    def reserve_ok(o: Order) -> None:
        print("[inventory] reserved")

    def pay_fail(o: Order) -> None:
        print("[payment] fail")
        raise RuntimeError("card declined")

    attempts = {"n": 0}

    def cancel_reserve_flaky(o: Order) -> None:
        attempts["n"] += 1
        if attempts["n"] < 3:
            print("[inventory] cancel reserve failed, retrying...")
            raise RuntimeError("inventory timeout")
        print("[inventory] reserve cancelled")

    o = Order(order_id="demo-1")
    o2 = run_saga(o, reserve=reserve_ok, pay=pay_fail, cancel_reserve=cancel_reserve_flaky)
    print("Result:", o2)
