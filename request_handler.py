from comments.request import create_comment, get_all_comments
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from posts import get_all_posts, get_posts_by_user, create_post
from categories import get_all_categories, create_category, delete_category
from users import get_all_users, get_user_by_email, create_user

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return (resource, key, value)

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

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

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "categories":
                if id is not None:
                    # response = get_single_animal(id)
                    pass
                else:
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
                    # response = get_single_location(id)
                    pass
                else:
                    response = get_all_comments()
                    

            if resource == "employees":
                if id is not None:
                    # response = get_single_employee(id)
                    pass
                else:
                    # response = get_all_employees()
                    pass

            if resource == "customers":
                if id is not None:
                    # response = get_single_customer(id)
                    pass
                else:
                    # response = get_all_customers()
                    pass

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            (resource, key, value) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "user_id" and resource == "posts":
                response = get_posts_by_user(value)
                
            if key == "email" and resource == "users":
                response = get_user_by_email(value)

            if key == "location_id" and resource == "animals":
                # response = get_animals_by_location_id(value)
                pass
            if key == "location_id" and resource == "employees":
                # response = get_employees_by_location_id(value)
                pass
            if key == "status" and resource == "animals":
                # response = f"{get_animals_by_status(value)}"
                pass
            
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

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.

        if resource == "login":
            new_item = get_user_by_email(post_body)

        if resource == "register":
            new_item = create_user(post_body)
            # pass
        if resource == "posts":
            new_item = create_post(post_body)
            # pass
        if resource == "categories":
            new_item = create_category(post_body)

        if resource == "comments":
            new_item = create_comment(post_body)
            
        if resource == "customers":
            # new_item = create_customer(post_body)
            pass


        self.wfile.write(f"{new_item}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        success = False
        # Delete a single animal from the list
        if resource == "animals":
            # update_animal(id, post_body)
            pass
        if resource == "customers":
            # update_customer(id, post_body)
            pass
        if resource == "employees":
            # update_employee(id, post_body)
            pass
        if resource == "locations":
            # update_location(id, post_body)
            pass

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "categories":
            delete_category(id)

        if resource == "locations":
            # delete_location(id)
            pass
        if resource == "employees":
            # delete_employee(id)
            pass
        if resource == "customers":
            # delete_customer(id)
            pass

        # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
