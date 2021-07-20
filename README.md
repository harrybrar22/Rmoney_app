# Rmoney_app

1. Run application locally:-

   a. install docker engine by following steps in below link:-
      windows:- https://docs.docker.com/docker-for-windows/install/
      Linux:- https://docs.docker.com/engine/install/ubuntu/
      Mac:- https://docs.docker.com/docker-for-mac/install/
      
   b. install docker compose to run docker compose file by gollowing steps in below link:-
      https://docs.docker.com/compose/install/
      
   c. download "docker-compose.yml" file in home directory of this application.
   
   d. In local system open terminal and browse to path of downloaded docker-compose file
   
   e. Now run command :- "docker-compose up"

   Note:- Before proceeding furthur please make sure docker-compose file is generating logs normally without any error message, also open url:- https://127.0.0.1:5000, if it shows "hello". It means your application is running successfully.
   
   
   
2. How to use this application:-

   a. Push stocks bhav copy in database:-
   
      Hit the API link:- https://127.0.0.1:5000/api/v1/bhav_copy/equity/<start_date>/<end_date>
      
      In this API we need to mention starting date and ending date, which determine the date interval of bhav copy need to be inserted.
      
      The date format should be :- "DD-MM-YYYY". (No other format will be accepted)


   b. Use Command to validate data:-
   
      Copy the data into folder:- /CSV_files/x    (x can be "stocks", "future_options")
      
      files can be placed by 
        "docker cp -R <source folder path> <flask contianer name>:/CSV_files/x"
   
      example:- 
        docker cp -R /mnt/d/files rmadmin_web_1:/CSV_files/stocks
      
  
      Check if all files are present in particular date range.
        "docker exec -it rmadmin_web_1 python3 manage.py check_files_stocks <start_date> <end_date>"
        Here date format -> "DD/MM/YYYY"
        for stocks -> "check_files_stocks" 
        It is generate logs of missing dates. Logs will be placed "Logs folder"
      Move log folder to desired system path
        docker cp -R <flask contianer name>:/Logs <destination path>
      example:- 
        docker exec -it rmadmin_web_1 python3 manage.py check_files_stocks 01/01/2020 31/12/2020
      
  
      Check Data integrity of files in data range:- 
        "docker exec -it rmadmin_web_1 python3 manage.py check_integrity_stocks <start_date> <end_date>"
        Here date format -> "DD/MM/YYYY"
        for stocks -> "check_integrity_stocks"
      Move log folder to desired system path
        docker cp -R <flask contianer name>:/Logs <destination path>
      example:- 
        "docker exec -it rmadmin_web_1 python3 manage.py check_integrity_stocks 01/01/2020 31/12/2020"
   
  
      
   
