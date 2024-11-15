import functions_framework

from google.cloud import firestore

db = firestore.Client(project="isbn-2024ii", database="isbn-tasks-db")

@functions_framework.http
def tasks_api(request):

    if request.method == 'POST':

        data = request.get_json()

        doc = db.collection("tasks").document(data['id'])
        doc.set(data['details'])

    return 'Task with id={} created!'.format(data['id']), 201