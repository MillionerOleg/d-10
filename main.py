import sys 
import requests    
 
# Я на всякий случай использовал данные из урока, но вы же можете вставить сюда свои, верно? :)
 auth_params = {    
    'key': "e3af0fe8e062b2b6ca5f9c906b8dc7fd",    
    'token': "08100766b52d1e38c68c2e6002abe277062726959a3126dae5a5dbb579ed2d3a", }
base_url = "https://api.trello.com/1/{}"
board_id = "y4ohsuNE" 

def read():            
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    for column in column_data:      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json() 

        # Нумерация
        print(column['name'] + " (" + str(len(task_data)) + ")")  

        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])    
    
def create(name, column_name):           
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
           
    for column in column_data:      
        if column['name'] == column_name: 
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})      
            break

# Колонки
def create_column(name):       
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    requests.post(base_url.format('lists'), data={'name': name, 'idBoard': column_data[0]['idBoard'], **auth_params})      


def move(name, column_name):  
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
          
    i = 1 
    task_id = None    
    task_list = {}

    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:
                # Создаю нумерованный словарь состоящий из словарей с информацией о задачах
                task_list[str(i)] = task
                # Сохраняю имя колонки
                task_list[str(i)]['col_name'] = column['name']
                i = i + 1

    # Если в словаре более 2-ух элементов, то пользователю предложат выбор
    if len(task_list) > 1:
        massage = "Выберите номер нужного варианта:\n"
        for num, task in task_list.items():
            # Подготовка сообщения для пользователя
            massage = massage + "{}\n\t{}. {} (ID - {})\n".format(task['col_name'],num, task['name'], task['id'])
        # Выбор будет записан в переменную task_id
        task_id = task_list[str(input(massage + ">>>"))]['id']
    else:
        task_id = task_list['1']['id']

    for column in column_data:    
        if column['name'] == column_name:    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break    
    
if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])
        # Создание колонок будет реализовано через команду "list"  
    elif sys.argv[1] == 'list':
        create_column(sys.argv[2])