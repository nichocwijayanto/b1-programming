import re
import logging

logging.basicConfig(
    filename='application_2.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' #used in %(asctime)s, for custom formatting. 
)

log_pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
r''' # r --> raw docstring. just to solve SyntaxWarning, not crucial. 
r' '    : raw string, backslash is treated literally.
()      : capture group. everything inside () is saved so it can be grabbed with .group()
\d+     : digit. matches one or more numbers (0-9).
\.      : literal period. since . usually means "any character", it uses \ to escape. 
.*?     : non-greedy match: matches any character but stops at the very first opportunity (e.g. the closing bracket ] ).
\[\]    : literal brackets: matches actual square brackets around the timestamp. 
\s      : space. In this pattern, actual spaces are used, which works too. 
'''

failed_logins = {}
total_lines = 0
incident_count = 0

try:
    with open("sample_log.txt", "r") as f_sam, \
        open("error_log.txt", "w") as f_err, \
        open("security_incidents.txt", "w") as f_sec:
        
        for line in f_sam:
            total_lines += 1
                    #re.search(pattern, string)
            match = re.search(log_pattern, line)    #match is an object, because returns multiple components from regex groupings. 
                                                    #therefore, it can be reached inside and grab specific parts of the log line. 

            if not match:
                logging.error(f"PARSING ERROR: Line does not match Apache format. Content: '{line.strip()}'")
                continue    # skips that line, onto the next line iteration.
            
            ip = match.group(1)
            timestamp = match.group(2)
            request = match.group(3)
            try:
                status_code = int(match.group(4))
            except (ValueError, TypeError) as e:    #e as container whichever error is triggered.
                logging.error(f"Data conversion error on line: {line.strip()} - Error: {e}")
                continue
            agent = match.group(7)

            if status_code >= 400:  #also captures 500
                f_err.write(line)
                logging.warning(f"HTTP {status_code} error recorded for IP {ip}. See 'error_log.txt' for further details.")
            
            #suspicious user agents
            if "sqlmap" in agent.lower() or "curl" in agent.lower():
                logging.warning(f"Suspicious activity from {ip}: {agent}")
                f_sec.write(f"[{timestamp}] ALERT: {ip} used suspicious agent: {agent}\n")
                incident_count += 1
            
            #failed authentication attempts
            if status_code == 401:
                failed_logins[ip] = failed_logins.get(ip, 0) + 1
                logging.info(f"Failed login attempt from {ip}")
                f_sec.write(f"[{timestamp}] FAILED AUTH: {ip}\n")

                #brute force attack detection
                if failed_logins[ip] > 3:
                    logging.warning(f"SECURITY ALERT: Brute force detected from {ip}")
                    f_sec.write(f"[{timestamp}] !!! BRUTE FORCE DETECTED !!! IP: {ip} has {failed_logins[ip]} failed attempts.\n")
                    incident_count += 1

except FileNotFoundError:
    logging.critical("Input file 'sample_log.txt' not found.")
    print("Error: The source log file is missing.")
except PermissionError:
    logging.error("Permission denied. Close the output files if they are open.")
    print("Error: Could not write reports. Check file permissions.")
except Exception as e:
    logging.critical(f"An unexpected error occurred: {e}")
    print(f"A critical error occurred. Check application_2.log.")

print("\n" + "="*30)
print("LOG ANALYSIS COMPLETE")
print("="*30)
print(f"Total entries processed:  {total_lines}")
print(f"Security incidents found: {incident_count}")
print(f"Errors captured:          (Check error_log.txt)")
print("="*30 + "\n")