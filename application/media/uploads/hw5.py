# definition of main

def main():
	
	print("This program will convert a base 10 number into another base ")
	
	# this variable is to check if the input is of true format
	
	check = True
	while check:
		# asking the user for input
	
		unsigned_number = input("Enter an unsigned integer: ")
		try:
			unsigned_number = int(unsigned_number)
			
			# if the user enters the negative number
			
			if unsigned_number >= 0:
				# ask again for input by giving check = False
				check = False
		except ValueError:
			check = True
	
	
	check = True
	
	# For maintaining the desired base initialized with 2
	Base = 2
	while check:
		# asking for the desired base
		choice = input("B for binary, O for octal, H for hexadecimal: ")
		
		# assigning Base according to the choice of user
		
		if choice == 'b' or choice == 'B':
			# assigning base 2
			
			Base = 2 
			check = False
		elif choice == 'o' or choice == 'O':
			#assigning base 8
			
			Base = 8 
			check = False
		elif choice == 'h' or choice == 'H':
			#assigning base 16
			
			Base = 16 
			check = False
		else:
			print("Invalid choice!  ")
			check = True
	
	# to store the final calculated answer
	final_answer = ""
	
	# main logic for converting
	
	while int(unsigned_number) != 0:
		# calculating remainder
		
		Remainder = unsigned_number % Base
		
		# for base 16 conversion if remainder is greater than 9 assign corresponding Alphabet
		if Remainder  == 10:
			final_answer += 'A'
		elif Remainder == 11:
			final_answer += 'B'
		elif Remainder == 12:
			final_answer += 'C'
		elif Remainder == 13:
			final_answer += 'D'
		elif Remainder == 14:
			final_answer += 'E'
		elif Remainder == 15:
			final_answer += 'F'
		else:
			final_answer += str(Remainder)
		
		# actual division
		unsigned_number =  int( unsigned_number / Base )
		
	# printing the answer
	print (str(final_answer)[::-1])
	
# main
	
if __name__ == "__main__":
	main()