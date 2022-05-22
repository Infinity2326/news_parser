from application import app


if __name__ == "__main__":
    app.secret_key = 'zk96D4Zjv8HkSaEdH2TSxD84Xwubwwss'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=False, use_reloader=False)
