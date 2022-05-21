from application import app


if __name__ == "__main__":
    app.secret_key = 'zk96D4Zjv8HkSaEdH2TSxD84Xwubwwsp'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, use_reloader=False)
