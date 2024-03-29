from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)

# CRUD
# Create, Read, Update and Delete = Criar, Ler, Atualizar, Deletar
# Tabela: Tarefa

tasks = []
task_id_control = 1


@app.post('/criar_task')
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control,
                    title=data['title'], description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso", "id": new_task.id}), 201


@app.get('/tasks')
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }
    return jsonify(output)


@app.get('/task/<int:id>')
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404


@app.put('/task/<int:id>')
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task == None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    return jsonify({"message": "Tarefa atualizada com sucesso"})


@app.delete('/task/<int:id>')
def delete_task(id: int):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

        if not task:
            return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)
