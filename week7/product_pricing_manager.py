import logging

logging.basicConfig(
    filename='application.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

discounts = {}
disc_amount = {}
final_list = []

try: 
    with open("products.txt", "r") as f: 
        logging.info("Successfully opened products.txt for reading.")
        #content = f.read()                     #not recommended for this lab
        #print(content)                         #bcs it treats the file content as one giant string. 

        for line in f:                          #this is better bcs it's iterated line-by-line, as a list of strings.            
            details = line.strip().split(",")   #gives one product at a time. 
            try: 
                base_price = float(details[1])
                logging.debug(f"Processed price for {details[0]}: {base_price}")
            except ValueError:
                logging.error(f"Invalid price format for '{details[0]}'. Line skipped.")
                continue

            #Category discounts: Electronics(10%), Clothing(15%), Books(5%), Home(12%)
            item = details[0]

            if details[2] == "Electronics":
                discounts[item] = 0.10
            elif details[2] == "Clothing":
                discounts[item] = 0.15
            elif details[2] == "Books":
                discounts[item] = 0.05
            elif details[2] == "Home":
                discounts[item] = 0.12

            #Tier discounts: Premium(+5%), Standard(no +), Budget(+2%)
            if details[3] == "Premium":
                discounts[item] = discounts.get(item, 0) + 0.05
                disc_amount['Amount'] = discounts[item] * base_price
            elif details[3] == "Standard":
                discounts[item] = discounts.get(item, 0) + 0
                disc_amount['Amount'] = discounts[item] * base_price
            elif details[3] == "Budget":
                discounts[item] = discounts.get(item, 0) + 0.02
                disc_amount['Amount'] = discounts[item] * base_price

            #Final Price per item
            disc_price = disc_amount['Amount']
            final = base_price * (1 - discounts[item])
            end_row = (item, base_price, discounts[item], disc_price, final)
            final_list.append(end_row)

except FileNotFoundError:
    logging.critical("File 'products.txt' missing. Program cannot proceed.")
    print("File not found. Check application.log for details.")

#Formatting output to a write on a file.
try: 
    with open("pricing_report.txt", "w") as f_out: 
        logging.info("Pricing report generated successfully.")
                                                                #file=f_out is an alternative for f.write(), for not having to add \n at each line. 
        print("\n=== FINAL ITEM PRICE (AFTER DISCOUNT) ===\n", file=f_out)   #this has print() behavior, auto \n at each line. but writes to the file. 
        print(
            f"{'Product Name':<25} | {'Base Price'} | "
            f"{'Discounts Applied'} | {'Discount Amount'} | "
            f"{'Final Price'} |", file=f_out
        )
        print("-" * 92, file=f_out)

        total_row = len(final_list)
        for i in range(total_row):
            print(
                f"{final_list[i][0]:<25} | €{final_list[i][1]:<9} | "
                f"{final_list[i][2]*100:>16.0f}% | €{final_list[i][3]:<14.2f} | "
                f"€{final_list[i][4]:<10.2f} |", file=f_out
            )
        print("\n", file=f_out)
except PermissionError:
    logging.error("Permission denied when writing to pricing_report.txt")
    print("Error: Access denied. Check application.log.")

#print a summary to console showing total products processed and average discount applied. 
print("\n=== STATISTICS ===")
print(f"\nTotal products processed: {total_row}")

if total_row > 0:
    avg_disc = sum(discounts.values()) / len(discounts)
    print(f"Average discount applied: {avg_disc * 100:.2f}% \n")
else:
    print("No valid products were found to calculate an average.")