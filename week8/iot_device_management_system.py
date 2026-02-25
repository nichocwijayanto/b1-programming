from datetime import datetime

class AuditLog:
    _entries = []

    @classmethod
    def write(cls, message):
        timestamp = datetime.now().isoformat()
        cls._entries.append(f"{timestamp} - {message}")

    @classmethod
    def show(cls):
        return "\n".join(cls._entries)

class User:
    def __init__(self, username, role):
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username must be non-empty.")
        if role not in ("admin", "standard"):
            raise ValueError("Role must be 'admin' or 'standard'.")
        
        self.username = username.strip()
        self.role = role

        AuditLog.write(f"User '{self.username}' created with role '{self.role}'")
    
    def get_username(self):
        return self.username
    
    def get_role(self):
        return self.role
    
    # Role check
    def is_admin(self):
        return self.role == "admin"

class Device:
    # parameter with default values should be in the very last order, to prevent SyntaxError.
    def __init__(self, device_id, device_type, firmware_version, owner, last_scan, compliance_status=True , is_active=True):
        if not isinstance(device_id, str) or not device_id.strip():
            raise TypeError("Device_id must be a string.")
        if not isinstance(device_type, str) or not device_type.strip():
            raise TypeError("Device_id must be a string.")
        if not isinstance(firmware_version, str) or not firmware_version.strip():
            raise TypeError("Device_id must be a string.")
        if not isinstance(owner, User):
            raise TypeError("The owner must be a valid User object.")
        
        self.device_id = device_id
        self.device_type = device_type
        self.__firmware_version = firmware_version
        self.__owner = owner
        self.__compliance_status = compliance_status
        self.__last_scan = last_scan
        self.__is_active = is_active

    # flip compliance_status to False, if last_scan > 30 days ago. 
    def check_compliance(self):
        days_since_scan = (datetime.now() - self.__last_scan).days

        if days_since_scan > 30:
            self.__compliance_status = False
            AuditLog.write(f"COMPLIANCE FAILURE: Device hasn't been scanned in {days_since_scan} days.")
            return False
        else:
            self.__compliance_status = True
            return True

    #only allow if the device is currently active (True).
    def update_firmware(self, new_version, requesting_user):  #requesting_user is a User object passed.
        if not self.__is_active:
            AuditLog.write(f"UPDATE FAILED: Attempted firmware update on quarantined device {self.device_id}")
            print(f"Error: Device {self.device_id} is quarantined. Update denied.")
            return False
        
        if requesting_user == self.__owner or requesting_user.get_role() == "admin":
            old_version = self.__firmware_version
            self.__firmware_version = new_version

            timestamp = datetime.now().isoformat()
            AuditLog.write(f"FIRMWARE UPDATE: {old_version} -> {new_version} by {requesting_user.get_username()} at {timestamp}")
            print(f"Success: Device {self.device_id} updated to version {new_version}.")
            return True
        else:
            AuditLog.write(f"UNAUTHORIZED UPDATE: {requesting_user.get_username()} tried to update {self.device_id}")
            print("Access Denied: You do not have permission to update this firmware.")
            return False


    # updates last_scan to current date and resets compliance_status to True. 
    def run_security_scan(self):
        self.__last_scan = datetime.now()
        self.__compliance_status = True
        timestamp = self.__last_scan.isoformat()
        AuditLog.write(f"Security scan completed at {timestamp}. Status: Compliant.")
        print(f"Scan complete for Device {self.device_id}")

    def authorise_access(self, user):
        # admin override: if user.privilege_level == 'admin' , grant access to ANY device regardless of owner. 
        if user.get_role() == "admin":
            AuditLog.write(f"ADMIN ACCESS: '{user.get_username()}' accessed device {self.device_id}")
            return True
        
        # ownership check: if not an admin, user must be the device.owner.
        if user != self.__owner:
            AuditLog.write(f"UNAUTHORIZED: '{user.get_username()}' attempted to access '{self.__owner.get_username()}'s device.")
            #msg = "Access Denied: You do not own this device."
            #print(msg)
            return False

        # compliance check: Even if owned, access is denied if device.compliance_status is False.
        if not self.__compliance_status:
            AuditLog.write(f"COMPLIANCE DENIAL: '{user.get_username()}' blocked due to non-compliant device.")
            #msg = "Access Denied: Device is non-compliant. Run security scan."
            #print(msg)
            return False
        
        # quarantine check: deny access if is_active = False. 
        if not self.__is_active:
            AuditLog.write(f"ACCESS DENIED for '{user.get_username()}', device {self.device_id} is quarantined.")
            #msg = "Device is quarantined. Access denied."
            #print(msg)
            return False

        return True

class DeviceManager:
    def __init__(self):
        self.__devices = []
    #devices = [] --> a list to store Device objects.

    def add_device(self, device):
        if isinstance(device, Device):
            self.__devices.append(device)
            AuditLog.write(f"Device {device.device_id} added to management system.")
        else:
            raise TypeError("Only Device objects can be added.")

    def remove_device(self, device):
        if not isinstance(device, Device):
            print("Error: Input must be a valid Device object.")
            return False

        if device in self.__devices:
            self.__devices.remove(device)
            AuditLog.write(f"Device {device.device_id} removed from management system.")
            print(f"Success: Device {device.device_id} has been removed.")
            return True
        else:
            print(f"Error: Device {device.device_id} is not managed by this system.")
            return False

    def quarantine_device(self, device_id, requesting_user):
        # Constraint: only 'Admin' can call this method. 
        if requesting_user.get_role() != "admin":
            AuditLog.write(f"SECURITY ALERT: {requesting_user.get_username()} attempted unauthorized quarantine.")
            print("Access Denied: Only administrators can quarantine devices.")
            return False

        #if the device_id given is not on the list, the loop finished with False for every single item. 
        for device in self.__devices:
            if device.device_id == device_id:
                # flips is_active to False. 
                device._Device__is_active = False 
                AuditLog.write(f"QUARANTINE: Device {device_id} disabled by '{requesting_user.get_username()}'.")
                print(f"Device {device_id} has been successfully quarantined.")
                return True
        
        #no else needed for this because anything after return statement is ignored. After return is executed, it exits the entire method. 
        print(f"Error: Device {device_id} not found.")
        return False

    #loops through devices list and prints a summary of all non-compliant or inactive devices. 
    def generate_report(self):
        print("\n" + "="*30)
        print("SYSTEM SECURITY REPORT")
        print("="*30)
        
        for device in self.__devices:
            # Trigger the 30-day compliance check logic
            device.check_compliance() 
            
            status = "ACTIVE" if device._Device__is_active else "QUARANTINED"
            compliance = "COMPLIANT" if device._Device__compliance_status else "NON-COMPLIANT"
            
            print(f"[{device.device_id}] Type: {device.device_type} | Status: {status} | Health: {compliance}")

        print("="*30 + "\n")

'''
In case of imports from another file within the same file:
- Everything inside this 'if' will ONLY run if you run Lab 1 directly.
- It will be ignored when you import the file into Lab 2. 
'''
if __name__ == "__main__":
    mallory = User("Mallory", "admin")
    alice = User("Alice", "standard")
    bob = User("Bob", "standard")

    manager = DeviceManager()
    camera = Device("CAM-01", "Security Camera", "v1.0", alice, datetime.now())
    
    manager.add_device(camera)

    print("\n--- Testing Access to Camera Device ---")
    print(f"Alice access: {camera.authorise_access(alice)}") 
    print(f"Bob access: {camera.authorise_access(bob)}") 
    print(f"Mallory access: {camera.authorise_access(mallory)}") 

    print("\n--- Testing Quarantine ---")
    manager.quarantine_device("CAM-01", mallory)
    print(f"Alice access after quarantine: {camera.authorise_access(alice)}")

    manager.generate_report()
    print("\n--- Final Audit Log ---")
    print(AuditLog.show())