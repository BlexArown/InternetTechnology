# Состояния заказа:
# NEW (создан), PAID (оплачен), DONE (завершен), CANCELLED (отменен)

# События (минимум для тестов):
# PAY_OK   -> оплата прошла
# PAY_FAIL -> оплата не прошла
# COMPLETE -> завершить заказ
# CANCEL   -> отменить заказ (ручная отмена/отмена по компенсации)

TRANSITIONS = {
    ("NEW", "PAY_OK"): "PAID",
    ("NEW", "PAY_FAIL"): "CANCELLED",

    ("PAID", "COMPLETE"): "DONE",
    ("PAID", "CANCEL"): "CANCELLED",

    # Если уже в финальном состоянии — остаёмся в нём
    ("DONE", "CANCEL"): "DONE",
    ("CANCELLED", "PAY_OK"): "CANCELLED",
    ("CANCELLED", "PAY_FAIL"): "CANCELLED",
    ("DONE", "PAY_OK"): "DONE",
    ("DONE", "PAY_FAIL"): "DONE",
}

FINAL_STATES = {"DONE", "CANCELLED"}

def next_state(state: str, event: str) -> str:
    # Если состояние финальное — никуда не двигаем
    if state in FINAL_STATES:
        return state

    # Если переход известен — применяем
    nxt = TRANSITIONS.get((state, event))
    if nxt is not None:
        return nxt

    # Неизвестное событие/переход — состояние не меняем
    return state
