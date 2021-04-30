from comments.request import create_comment, get_all_comments
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from posts import get_all_posts, get_posts_by_user, create_post, delete_post
from users import get_all_users, get_user_by_email, create_user
from categories import get_all_categories, create_category, delete_category
from tags import create_tag


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            param = resource.split("?")[1]  
            resource = resource.split("?")[0]  
            pair = param.split("=")  
            key = pair[0] 
            value = pair[1]  

            return (resource, key, value)

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  
            except ValueError:
                pass 

            return (resource, id)

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)


        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "categories":
                response = get_all_categories()

            if resource == "posts":
                if id is not None:
                    # response = get_single_post(id)
                    pass
                else:
                    response = get_all_posts()

            if resource == "users":
                if id is not None:
                    pass
                else:
                    response = get_all_users()

            if resource == "comments":
                if id is not None:
                    pass
                else:
                    response = get_all_comments()

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "user_id" and resource == "posts":
                response = get_posts_by_user(value)

            if key == "email" and resource == "users":
                response = get_user_by_email(value)


        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new item
        new_item = None

        if resource == "login":
            new_item = get_user_by_email(post_body)

        if resource == "register":
            new_item = create_user(post_body)

        if resource == "posts":
            new_item = create_post(post_body)
        
        if resource == "categories":
            new_item = create_category(post_body)

        if resource == "tags":
            new_item = create_tag(post_body)

        if resource == "comments":
            new_item = create_comment(post_body)

        self.wfile.write(f"{new_item}".encode())

    def do_PUT(self):

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        success = False

        # if resource == "posts":
            # update_post(id, post_body)
            # pass

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new resource and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "posts":
            delete_post(id)

        if resource == "categories":
            delete_category(id)

        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
