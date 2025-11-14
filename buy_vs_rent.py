def compute_curr_buyer_wealth(condoValue, loanOutstanding, buyerPortfolio):
    return condoValue - loanOutstanding + buyerPortfolio

def compute_buyer_annual_costs(condoPrice, monthlyMorguage, hoaFee, propertyTax, repair_percentage):
     return (monthlyMorguage * 12) + (hoaFee * 12) + propertyTax + (condoPrice * repair_percentage) + (condoPrice * insurance_rate)

def compute_curr_renter_wealth(currRenterWealth, annualCostBuyer, rent, marketReturnRate):
    return currRenterWealth + max(0, annualCostBuyer - (rent * 12)) * marketReturnRate # The leftover money from not buying, with the investment return rate applied to it. 

# [P] principle - [r] annual interest rate - [n] loan term in years 
def total_mortgage_interest(P, r, n, payments_per_year=12): 
    periodic_rate = r / payments_per_year
    total_payments = n * payments_per_year
    A = P * (periodic_rate * (1 + periodic_rate)**total_payments) / ((1 + periodic_rate)**total_payments - 1)
    total_paid = A * total_payments
    total_interest = total_paid - P
    return total_interest


### ----- Input ----- ### 

#Take in listing and payment information
print("\nUNIT INFORMATION:\n")
condo_price = int(input("\tEnter CONDO PRICE: $"))
start_hoa_fee = int(input("\tEnter HOA FEE: $"))
start_property_tax = int(input("\tEnter ANNUAL PROPERTY TAX: $"))
start_rent = int(input("\n\tEnter MONTHLY RENT OF COMPARISON UNIT: $"))

print("\n\nMORGUAGE INFORMATION:\n")
mr = float(input("\tEnter MORGUAGE INTEREST RATE (%) -> NON-DECIMAL: "))
d_payment = int(input("\tEnter DOWN PAYMENT: $"))
num_y = int(input("\tEnter MORGUAGE TERM (YEARS): "))

print("\n\nMARKET PREDICTIONS:\n")
pa = float(input("\tEnter PREDICTED CONDO APPRECIATION RATE (%) -> NON-DECIMAL: "))
irr = float(input("\tEnter PREDICTED INVESTMENT RETURN RATE (STOCKS/BONDS/CD's etc...) (%) -> NON-DECIMAL: "))



### ----- Ajust Input Values ----- ### 

# Copy the starting hoa, property tax, and rent rate since they will be increasing. 
hoa_fee = start_hoa_fee
property_tax = start_property_tax
rent = start_rent 

# Divide the morguage interest rate by 100 since they will be multiplied by the cost of the condo. 
m_rate = mr / 100 

# Format the market return rate and property appreciation rate, as in-face, and appreciating rate
marketReturnRate = 1 + (irr / 100) 
property_appreciation_rate = 1 + pa / 100

# Create a list of integers, each representing a year in the morguage term. Start at 0, go to the year - 1
years = []
for year_e in range(num_y):
      years.append(year_e)

### ----- Assumptions ----- ###
 
rent_increase = 1.04
hoa_increase_rate = 1.04
property_tax_increase_rate = 1.05

repair_percentage = 0.0125  # Annual percetage of the condo's value set aside for repairs and special assessments 
one_off_costs = 0.05      # One-off initial costs to buy, percentage of the condo's value 
selling_cost_rate = 0.07  # One-off costs to sell, percentage of the condo's value
insurance_rate = 0.0025



### ----- Calculations ----- ### 
wealth_buyer = []
wealth_renter = []
condoValueHistory = []
rentRateHistory = []
loanOutstandingHistory = []
annualCostHistory = []
extraToInvestHistory = []

buyerPortfolio = 0
totalPaidInRent = 0

loan_amount = condo_price - d_payment
init_wealth_buyer = condo_price - loan_amount 
init_wealth_renter = d_payment + (one_off_costs * condo_price)
total_money_put_in = (condo_price * one_off_costs) + (condo_price * repair_percentage)

currCondoValue = condo_price
currRentRate = rent
currLoanOutstanding = loan_amount
currHOA_FEE = hoa_fee
currPROPERTY_TAX = property_tax
currRenterWealth = init_wealth_renter
currBuyerWeatlh = init_wealth_buyer


totalInterestPaid = total_mortgage_interest(loan_amount, m_rate, num_y)
currLoanOutstanding = currLoanOutstanding + totalInterestPaid
monthlyMorguage = currLoanOutstanding / (num_y * 12)

# For each year in the morgugae term... 
for year in years:

      # ... record a snapshot of the current year's condo value, rent rate, and amount outstanding on the loan. 
      condoValueHistory.append(currCondoValue)
      rentRateHistory.append(currRentRate)
      loanOutstandingHistory.append(currLoanOutstanding)

      # ... add the total rent paid, and total morguage interest paid, for the given year, to their running counts.    
      totalPaidInRent = totalPaidInRent + (currRentRate * 12)

      # ... compute the total annual costs of the buyer. 
      annualCostBuyer = compute_buyer_annual_costs(currCondoValue, monthlyMorguage, currHOA_FEE, currPROPERTY_TAX, repair_percentage)

      # ... record a snapshot of buyer's metrics.
      wealth_buyer.append(currBuyerWeatlh)
      annualCostHistory.append(annualCostBuyer)
      total_money_put_in = total_money_put_in + annualCostBuyer

      # ... record snapshot of renter's metrics. 
      leftover = max(0, annualCostBuyer - (currRentRate * 12))
      extraToInvestHistory.append(leftover)
      wealth_renter.append(currRenterWealth)
      
      # ... adjust current wealth and buyer wealth, for next year.  
      currBuyerWeatlh = compute_curr_buyer_wealth(currCondoValue, currLoanOutstanding, buyerPortfolio)
      currRenterWealth = compute_curr_renter_wealth(currRenterWealth, annualCostBuyer, currRentRate, marketReturnRate)

      # ... adjust condo value, rent rate, loan outstanding, hoa fee, and property tax for next year. 
      currCondoValue = currCondoValue * property_appreciation_rate 
      currRentRate = currRentRate * rent_increase
      currLoanOutstanding = currLoanOutstanding - (monthlyMorguage * 12)
      currHOA_FEE = currHOA_FEE * hoa_increase_rate
      currPROPERTY_TAX = currPROPERTY_TAX * property_tax_increase_rate


 
currBuyerWeatlh = compute_curr_buyer_wealth(currCondoValue, currLoanOutstanding, buyerPortfolio)
currRenterWealth = compute_curr_renter_wealth(currRenterWealth, annualCostBuyer, currRentRate, marketReturnRate)
num_y = num_y + 1

wealth_renter.append(currRenterWealth)
wealth_buyer.append(currBuyerWeatlh)

# ----- Report ----- 

# Assumptions formatting
pt_i = (property_tax_increase_rate - 1) * 100
hoa_i = (hoa_increase_rate - 1) * 100
rent_i = (rent_increase - 1) * 100
sc = selling_cost_rate * 100
bc = one_off_costs * 100 
rp = repair_percentage * 100
ir = insurance_rate * 100

# Result summary formatting 
total_m_cost = totalInterestPaid + condo_price
final_property_value = currCondoValue
total_money_put_in = total_money_put_in + (currCondoValue * selling_cost_rate)
total_unrecoverable_costs = total_money_put_in - final_property_value
total_unrecoverable_costs_monthly = total_unrecoverable_costs / (num_y * 12)
loss_liquid_captial = total_money_put_in - totalPaidInRent
equity_weight = (final_property_value / total_money_put_in) * 100
amoratized_rent = (totalPaidInRent / num_y) / 12

# Analytics Section 
print("\n\nAnalytics: [BUYER | RENTER]\n")

j = 0
already_brokeven = False 
for currVal, currOut, currP, currR, currI in zip(condoValueHistory, loanOutstandingHistory, annualCostHistory, rentRateHistory, extraToInvestHistory):
     currP = currP / 12
     print(f"Year{j:3}:  Condo Value: ${currVal:<8,.0f} {'':>4} Loan Outstanding: ${currOut:,.0f} {'':>4} Monthly Payment: ${currP:,.0f}/mo {'|':>4} Rent: ${currR:,.0f}/mo {'':>4} Leftover To Invest: ${currI:,.0f}\n")
     j += 1

print("\nWealth: Year By Year\n")
i = 0
already_brokeven = False 
for w_buyer, w_renter in zip(wealth_buyer, wealth_renter):
     if not already_brokeven and w_buyer >= w_renter:
        print(" ------------------------------ BREAK-EVEN ------------------------------ \n")
        already_brokeven = True
     print(f"Year{i:3}:        Wealth Buyer = {w_buyer:<8,.0f} {'':>10}   Renter Portfolio = {w_renter:,.0f}\n")

     i += 1

# Report 
print("\nInput Summary:\n")
print(f"CONDO COST:  \t${condo_price:,.0f}")
print(f"HOA FEE:     \t${start_hoa_fee}/mo")
print(f"PROPERTY TAX:\t${start_property_tax:,}/yr\n")
print(f"DOWN PAYMENT             \t${d_payment:,}")
print(f"MORGUAGE INTEREST RATE:  \t{m_rate * 100:.2f}%")
print(f"CONDO APPRECIATION RATE: \t{pa:.2f}%")
print(f"INVESTMENT RETURN RATE:  \t{irr:.2f}%\n")

print("\nAssumptions Made:\n")
print(f"PROPERTY TAX ANNUAL INCREASE RATE:                                     \t{pt_i:.2f}%")
print(f"HOA ANNUAL INCREASE RATE:                                              \t{hoa_i:.2f}%")
print(f"RENT ANNUAL INCREASE RATE:                                             \t{rent_i:.2f}%\n")
print(f"COST TO BUY (PERCENT OF PROPERTY VALUE):                               \t{bc:.2f}%")
print(f"COST TO SELL (PERCENT OF PROPERTY VALUE):                              \t{sc:.2f}%")
print(f"ANNUAL PERCENT OF PROPERTY VALUE (FOR REPAIRS & SPECIAL-ASSESSMENTS):  \t{rp:.2f}%")
print(f"ANNUAL PERCENT OF PROPERTY VALUE FOR YEARLY INSURANCE COSTS:           \t{ir:.2f}%")

print("\n\nResult Summary:\n")
print(f"PROPERTY VALUE AFTER {num_y} YEARS:         \t${final_property_value:,.0f}")
print(f"TOTAL SPENT ON CONDO AFTER {num_y} YEARS:   \t${total_money_put_in:,.0f}")
print(f"TOTAL PAID IN RENT OVER {num_y} YEARS:      \t${totalPaidInRent:,.0f}")
print(f"TOTAL LOSS OF LIQUID CAPTIAL:           ${loss_liquid_captial:,.0f}\n")

print(f"TOTAL MORGUAGE COST:       \t${total_m_cost:,.0f}")
print(f"TOTAL INTEREST PAID:       \t${totalInterestPaid:,.0f}")
print(f"TOTAL UNRECOVERABLE COSTS: \t${total_unrecoverable_costs:,.0f}  |  ${total_unrecoverable_costs_monthly:,.0f}/mo  |  Asset Recovery Weight: {equity_weight:,.0f}%")
print(f"TOTAL RENT PAID:           \t${totalPaidInRent:,.0f}  |  ${amoratized_rent:,.0f}/mo <-- (average rate over {num_y} years.)")

print("\n")
print(f"Compared against an apartment costing ${start_rent}/mo (on year 1)\n")
if w_buyer >= w_renter:
     difference = w_buyer - w_renter
     y = years[len(years)-1]
     print(f"RESULT: BUYER WEALTHIER BY ${difference:,.0f} at year {y+1}")
else:
     y = years[len(years)-1]
     difference = w_renter - w_buyer
     print(f"RESULT: RENTER WEALTHIER BY ${difference:,.0f} at year {y+1}")

print("\n")


