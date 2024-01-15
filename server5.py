from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import urllib.parse

class EmployeeServer(BaseHTTPRequestHandler):
    DATA_FILE = "data.csv"

    def _load_data(self):
        try:
            with open(self.DATA_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_data(self, data):
        with open(self.DATA_FILE, 'w') as file:
            json.dump(data, file, indent=2)

    def _get_employee_by_name(self, name):
        data = self._load_data()
        for employee in data:
            if employee['name'] == name:
                return employee
        return None

    def _respond(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    def do_POST(self):
        if self.path == "/employees":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                employee_data = json.loads(post_data)
            except json.JSONDecodeError:
                self._respond(400, "Invalid JSON format. Valid format example: {'name': 'John', 'age': 25, 'address': 'New York'}")
                return

            if 'name' not in employee_data or 'age' not in employee_data or 'address' not in employee_data:
                self._respond(400, "Name, age, and address are required in the request body.")
                return

            employee_name = employee_data['name']
            existing_employee = self._get_employee_by_name(employee_name)
            if existing_employee:
                self._respond(409, "Data resource already exists. Use PUT to update data.")
                return

            
            employee_data['id'] = len(self._load_data()) + 1

            if 'is_active' not in employee_data:
                employee_data['is_active']=True

            data = self._load_data()
            data.append(employee_data)
            self._save_data(data)

            self._respond(200, "Data resource created successfully.")
        else:
            self._respond(404, "Invalid path.")
    
    def do_GET(self):
        all_emp_data={}
        out=[]
        emp_data={}
        if self.path == "/employees":
            data = self._load_data()
            parsed_path=urllib.parse.urlparse(self.path)
            query_param=urllib.parse.parse_qs(parsed_path.query)
            
            try:
                if 'is_active' not in query_param:
                    
                    all_emp_data["employees"]=data
                    response=json.dumps(all_emp_data)
                    self._respond(200,response)
                    
                elif query_param['is_active']==True:
                    for i in data:
                        if i['is_active']==True:
                                out.append(i)
                    all_emp_data["employees"]=out
                    d=json.dumps(all_emp_data)            
                    self._respond(200,d)
                else:
                    for i in data:
                        if i['is_active']==False:
                                out.append(i)
                    all_emp_data["employees"]=out
                    d=json.dumps(all_emp_data)            
                    self._respond(200,d)
            except:
                self._respond(500, "Invalid value for 'is_active' parameter.")

        elif self.path.startswith("/employees/"):
           _, _,name = self.path.rpartition("/")
           try:
                employee=self._get_employee_by_name(name)
                if employee:
                    emp_data["data"]=employee
                    d=json.dumps(emp_data)
                    self._respond(200,d)
                else:
                    self._respond(404,"Data resource not created. Use POST to create data first.")
           except:
                self._respond(500, "Error while accessing data resource..")
        else:
        
            self._respond(404, "Invalid path.")
    
    def do_PUT(self):
        if self.path.startswith("/employees/"):
            _, _, employee_name = self.path.rpartition("/")
            existing_employee = self._get_employee_by_name(employee_name)
            
            if not existing_employee:
                self._respond(404, "Data resource not created. Use POST to create data first.")
                return
            
            
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length).decode('utf-8')

            try:
                updated_data = json.loads(put_data)
            except json.JSONDecodeError:
                self._respond(400, "Invalid JSON format. Valid format example: {'age': 30, 'address': 'Updated Address'}")
                return
            
            data = self._load_data()
            for i in data:
                   if i==existing_employee:
                        for j in updated_data:
                             if j in i:
                                  i[j]=updated_data[j]
                                
            self._save_data(data)

            self._respond(200, "Data resource updated successfully.")
        else:
            self._respond(404, "Invalid path.")
            
    def do_DELETE(self):
        if self.path.startswith("/employees/"):
            _, _, employee_name = self.path.rpartition("/")
            existing_employee = self._get_employee_by_name(employee_name)
            try:
                if not existing_employee:
                    self._respond(404, "Data resource not created. Use POST to create data first.")
                    return

                data = self._load_data()
                data.remove(existing_employee)
                self._save_data(data)
            
                self._respond(200, "Employee deleted successfully.")
            except:
                self._respond(500, "Error while accessing data resource..")
        else:
            self._respond(404, "Invalid path.")


       
    
if __name__ == '__main__':
    port = 9090
    server_address = ('', port)

    try:
        httpd = HTTPServer(server_address, EmployeeServer)
        print(f"Server running on port {port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

