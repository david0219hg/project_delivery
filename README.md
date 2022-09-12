# Running the project
- First have docker and docker-compose installed, then run docker compose up -d 
- then the project will be running, for runing the test get inside the docker container that is running 
   with docker exec -it <container_name> bash
   and run pytest for running the test

# how the project works
- First, if there is any doubt the test could help a lot for the understanding


- For creating a driver 

body :    
        "free": True,
        "latitude_driver": 15,
        "length_driver": 15,
        "updated_at": datetime.datetime.now()
http verb: post
end_point: "/driver/"

- For updating drivers (important that the ones that are gonna be updated from the external json API have  already been created with the respective ids that are sent from the external API)

http verb: put
end_point: "/driver/"

- For assigning order to driver 

body :
    "date_time_arrive": datetime.datetime(2015, 10, 1, 20, 0, 0, 0),
    "date_time_delivery": datetime.datetime(2015, 10, 1, 21, 0, 0, 0),
    "latitude_arrrive": 30,
    "length_arrrive": 30,
    "latitude_delivery": 60,
    "length_delivery": 45

http verb: put
endpoint : "/driver/assign/order/{driver.id}/"

- For getting order by day and ordered by hour 
endpoint : "/driver/assing/order/list/?day=1

- For getting order by driver and day 
http verb: get
endpoint: /driver/assing/order/list/?day=1&driver={driver.id}

- Get nearest driver
http verb: get
endpoint: /driver/nearlocation/?lattitude=50&length=50&date=2021-12-10&hour=0