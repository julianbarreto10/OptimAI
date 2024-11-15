from flask import Flask, request, jsonify
from data_adquisition.data import fetch_routing_data
from cal_statistics.stats import calculate_statistics
import config

app = Flask(__name__)


@app.route('/stats', methods=['GET'])
def get_routing_stats():
    # Obtener el nombre del cliente desde los parámetros
    cliente = request.args.get('cliente')
    if not cliente:
        return jsonify({"error": "Parámetro 'cliente' es requerido"}), 400

    # Obtener los datos de enrutamiento del cliente
    routing_data = fetch_routing_data(cliente, config.URL_DB_GET)

    if not routing_data:
        return jsonify({"error": "No se encontraron datos para el cliente especificado"}), 404

    # Calcular las estadísticas
    stats = calculate_statistics(routing_data)

    # Devolver el resultado en formato JSON
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
