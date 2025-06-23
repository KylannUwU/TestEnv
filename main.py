from flask import Flask, request
import os

app = Flask(__name__)

plans = []  # Lista dinámica de planes
current_plan_index = -1  # Índice del plan actual "En pantalla"
call_participants = []  # Participantes de la llamada
DEFAULT_CALL = {"name": "Solita", "emote": "nephuLurk"}  # Llamada por defecto


@app.route("/addplan")
def add_plan():
    global plans, current_plan_index

    raw_input = request.args.get("plan", "").strip()

    if not raw_input:
        return "No se recibieron planes."

    items = [item.strip() for item in raw_input.split(",") if item.strip()]
    set_flag = False
    insert_pos = None
    cleaned_items = []

    for item in items:
        local_set_flag = False
        local_insert_pos = None

        if "-set" in item:
            local_set_flag = True
            item = item.replace("-set", "").strip()

        if "-pos" in item:
            try:
                parts = item.split("-pos")
                item = parts[0].strip()
                local_insert_pos = int(parts[1].strip()) - 1
            except:
                return "Parámetro -pos inválido."

        cleaned_items.append((item, local_insert_pos, local_set_flag))

    for index, (plan, pos, do_set) in enumerate(cleaned_items):
        insert_index = pos if pos is not None else len(plans)
        insert_index = max(0, min(insert_index, len(plans)))
        plans.insert(insert_index, plan)

        if do_set:
            current_plan_index = insert_index
        elif set_flag and index == 0:
            current_plan_index = insert_index

    return f"Planes añadidos: {', '.join([p[0] for p in cleaned_items])}"


@app.route("/removeplan")
def remove_specific_plans():
    global current_plan_index

    plans_to_remove_raw = request.args.get("plan", "")
    if not plans_to_remove_raw:
        return "No se especificaron planes para remover."

    plans_to_remove = [p.strip().lower() for p in plans_to_remove_raw.split(",") if p.strip()]
    removed_plans = []

    i = 0
    while i < len(plans):
        plan_lower = plans[i].lower()
        if plan_lower in plans_to_remove:
            removed = plans.pop(i)
            removed_plans.append(removed)
            if current_plan_index == i:
                current_plan_index = -1
            elif current_plan_index > i:
                current_plan_index -= 1
        else:
            i += 1

    if removed_plans:
        return f"Planes removidos: {', '.join(removed_plans)}"
    else:
        return "Plan no existente nephuThink"


@app.route("/setplan")
def set_plan():
    global current_plan_index
    plan_to_set = request.args.get("plan", "").strip().lower()
    for i, plan in enumerate(plans):
        if plan.lower() == plan_to_set:
            current_plan_index = i
            return f"'{plans[i]}' En pantalla nephuo7"
    return "Plan no encontrado nephuThink"


@app.route("/nextplan")
def next_plan():
    global current_plan_index
    if current_plan_index == -1:
        return "No hay plan en pantalla actualmente."
    elif current_plan_index + 1 >= len(plans):
        return "Ya estás en el último plan nephuThink"
    else:
        current_plan_index += 1
        return f"Siguiente plan: {plans[current_plan_index]} [En pantalla] nephuo7"


@app.route("/resetplan")
def reset_plan():
    global plans, current_plan_index
    plans.clear()
    current_plan_index = -1
    return "Planes reiniciados nephuComfy"


@app.route("/plan")
def get_plan():
    user = request.args.get("user", "alguien")
    parts = []

    for i, plan in enumerate(plans):
        if i < current_plan_index:
            parts.append(f"{plan} [✓]")
        elif i == current_plan_index:
            parts.append(f"{plan} [En pantalla ]")
        else:
            parts.append(plan)

    dynamic_part = " ➜ ".join(parts) + " ➜ " if parts else ""
    return f"nephuPats Plan nephuUwu  [ Plan de Hoy ] ➜ {dynamic_part}Mucho Más! nephuPls @{user}"


@app.route("/addcall", methods=['GET'])
def add_call():
    entries = request.args.get("entries", "").split()
    if len(entries) % 2 != 0:
        return "Numero incorrecto de elementos, recuerda enviar siempre un Nombre sin espacios y un Emote por participante nephuDerp"

    for i in range(0, len(entries), 2):
        name = entries[i]
        emote = entries[i + 1]
        call_participants.append({"name": name , "emote": emote})

    return f"Participantes añadidos: {' , '.join([f'{name} {emote}' for name, emote in zip(entries[::2], entries[1::2])])}"


@app.route("/removecall", methods=['GET'])
def remove_call():
    names = request.args.get("entries", "").split()
    removed = []
    names = [name.lower() for name in names]

    for name in names:
        for participant in call_participants[:]:
            if participant['name'].lower() == name:
                call_participants.remove(participant)
                removed.append(f"{participant['name']} {participant['emote']}")

    if not call_participants:
        return f"{DEFAULT_CALL['name']} {DEFAULT_CALL['emote']}" 

    if removed:
        return f"Participantes removidos: {' , ' .join(removed)}"
    else:
        return "No se encontraron participantes para remover."


@app.route("/resetcall", methods=['GET'])
def reset_call():
    call_participants.clear()
    return f"!call reiniciado nephuComfy"


@app.route("/call", methods=['GET'])
def get_call():
    if not call_participants:
        return f"{DEFAULT_CALL['name']} {DEFAULT_CALL['emote']}"

    call_info = " ".join([f"{p['name']} {p['emote']}" for p in call_participants])
    return call_info


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
