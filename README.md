# A example flask web api application 

### How to start application

1. Create and fire up your virtual environment in python3
2. Install requirements
    ```sh
    pip install -r requirements.txt
    ```
3. Create database (You can use database info from config.py)
4. Use command for apply the migration to the database
    ```sh
    python manage.py db upgrade
    ```
### Available api methods
1. Get all forms.
     - url : /api/v0/form
     - method: GET
     
2. Create form.
     - url : /api/v0/form
     - method: POST
     - Parameters: 
        - name : string
     - Example json for send:
        ```json
        {
            "name": "Profile form"
        }
        ```
3. Get field types.
     - url : /api/v0/field
     - method: GET
     
4. Add field to form.
     - url : /api/v0/field
     - method: POST
     - Parameters: 
        - name : string
        - form_id : int 
        - type : string (get from available field types)
     - Example json for send:
        ```json
            {
            	"name" : "age",
            	"type" : "number",
            	"form_id": 1
            }
        ```
        
5. Get detail information about form:
     - url : /api/v0/form/(<id:int>) 
      (where id is form id)
     - method: GET
     
6. Submit Form.
     - url : /api/v0/form/(<id:int>)/submit 
     (where id is form id)
     - method: POST
     - Parameters: 
        List of fields. Field has paramameters:
        - id : int
        - type : string
        - value : string (if you choose text type) or int (if you choose number type)         or date string should be in format YYYY-MM-DD (if you choose date type)
     - Example json for send:
        ```json
        {
         "fields": [
                {
                    "id": 1,
                    "type_field": "date",
                    "value": "2018-06-06"
                },
                {
                    "id": 2,
                    "type_field": "number",
                    "value": 20
                },
                {
                    "id": 3,
                    "type_field": "text",
                    "value": "Test"
                }
            ]
        }
        ```