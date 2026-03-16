
def bookish_routes(app):
    @app.route('/healthcheck')
    def health_check():
        return {"status": "OK"}

