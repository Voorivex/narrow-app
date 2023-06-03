from flask import Flask, request, render_template, jsonify, abort

app = Flask(__name__)

users = {
    "user1": {
        "email": "user1@example.com",
        "username": "User1",
        "info": "User 1 information"
    },
    "user2": {
        "email": "user2@example.com",
        "username": "User2",
        "info": "User 2 information"
    },
    "user3": {
        "email": "user3@example.com",
        "username": "User3",
        "info": "User 3 information"
    }
}

admins = {
    "admin_user": {
        "email": "admin@example.com",
        "username": "Admin",
        "info": "Admin information"
    }  
}

admin_content = "This is the administration content."

@app.route('/')
def index():
    if 'x-requested-with' in request.headers:
        abort(500)

    frog_user = request.headers.get('x-fb')
    return render_template('index.html', frog_user=frog_user)

@app.route('/users')
def user_list():
    return render_template('user_list.html', users=users)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        return render_template('thank_you.html')

    email = request.args.get('email', '')
    return render_template('contact.html', email=email)

@app.route('/api/user/<user_hash>')
def user_info(user_hash):
    if user_hash in users:
        return jsonify(users[user_hash])
    else:
        return jsonify({"error": "User not found."}), 404

@app.route('/api/users/all')
def all_users_info():
    return jsonify([users, admins])

@app.route('/admins_panel')
def admin():
    debug = request.args.get('debug')
    if debug == 'true':
        return admin_content
    else:
        return "403 Forbidden", 403

@app.route('/show-http-packet')
def show_http_packet():
    http_packet = ''
    environ = request.environ
    # Retrieve the necessary environment variables
    request_method = environ['REQUEST_METHOD']
    script_name = environ['SCRIPT_NAME']
    path_info = environ['PATH_INFO']
    query_string = environ['QUERY_STRING']
    server_protocol = environ['SERVER_PROTOCOL']

    # Construct the request line
    request_line = f"{request_method} {script_name}{path_info}?{query_string} {server_protocol}\r\n"
    http_packet += request_line

    # Add the request headers
    for key, value in environ.items():
        if key.startswith('HTTP_'):
            header_name = key[5:].replace('_', '-')
            header_line = f"{header_name}: {value}\r\n"
            http_packet += header_line

    # Add an empty line to separate headers from body
    http_packet += "\r\n"

    # Add the request body if present
    if request_method == 'POST':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(content_length).decode('utf-8')
        http_packet += request_body

    print(http_packet)
    return 'Yo!'

if __name__ == '__main__':
    app.run()