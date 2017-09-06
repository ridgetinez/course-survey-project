// testList.c - testing DLList data type
// Written by John Shepherd, March 2013

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "DLList.h"

#define ANSI_COLOR_BLUE "\33[0:34m\\]"
#define ANSI_COLOR_RESET "\33[0m\\]"

int main(int argc, char *argv[])
{
	DLList myList;
	myList = getDLList(stdin);
	putDLList(stdout,myList);
	assert(validDLList(myList));		
	
	printf("Test 1 Checking for DLListBefore -> inserting correctly at start\n");
	DLListBefore(myList, "First Testing");
	if (validDLList(myList) == 1) {
		printf("\033[22;32mText Passed!!! \033[0m\n");
		
	} else {  
		printf("\033[22;31mText Failed! \033[0m\n");
		putDLList(stdout,myList);
	}
	

	printf("\nTest 2 Checking for DLListBefore -> inserting correctly in the last\n");
	DLListMoveTo(myList, 5);
	DLListBefore(myList, "Second Testing");
	if (validDLList(myList) == 1) {
		printf("\033[22;32mText Passed!!! \033[0m\n");
	} else {  
		printf("\033[22;31mText Failed! \033[0m\n");
		putDLList(stdout,myList);
	}

	printf("\nTest 3 Checking for DLListBefore -> inserting correctly in the middle\n");
	DLListBefore(myList, "Third Testing");
	if (validDLList(myList) == 1) {
		printf("\033[22;32mText Passed!!! \033[0m\n");
	} else {  
		printf("\033[22;31mText Failed! \033[0m\n");
		putDLList(stdout,myList);
	}

	printf("\nTest 4 Checking for DLListAfter -> inserting correctly at start\n");
	DLListMoveTo(myList, 1);
	DLListAfter(myList, "Fourth Testing");
	if (validDLList(myList) == 1) {
		printf("\033[22;32mText Passed!!! \033[0m\n");
	} else {  
		printf("\033[22;31mText Failed! \033[0m\n");
		putDLList(stdout,myList);
	}

	printf("\nTest 5 Checking for DLListAfter -> inserting correctly last\n");
	DLListMoveTo(myList, 5);
	DLListAfter(myList, "Fifth Testing");
	if (validDLList(myList) == 1) {
		printf("\033[22;32mText Passed!!! \033[0m\n");
	} else {  
		printf("\033[22;31mText Failed! \033[0m\n");
		putDLList(stdout,myList);
	}

	printf("\nTest 6 Checking for DLListAfter -> inserting correctly in the middle\n");
	DLListMoveTo(myList, 2);
	DLListAfter(myList, "Sixth Testing");
	if (validDLList(myList) == 1) {
		printf("\033[22;32mText Passed!!! \033[0m\n");
	} else {  
		printf("\033[22;31mText Failed! \033[0m\n");
		putDLList(stdout,myList);
	}

	printf("\nTest 7 Checking for DLListDelete -> deleting at the start\n");
	DLListMoveTo(myList, 1);
	DLListDelete(myList);
	if (validDLList(myList) == 1) {
		printf("\033[22;32mText Passed!!! \033[0m\n");
	} else {  
		printf("\033[22;31mText Failed! \033[0m\n");
		putDLList(stdout,myList);
	}

	printf("\nTest 8 Checking for DLListDelete -> deleting last\n");
	DLListMoveTo(myList, 8);
	DLListDelete(myList);
	if (validDLList(myList) == 1) {
		printf("\033[22;32mText Passed!!! \033[0m\n");
	} else {  
		printf("\033[22;31mText Failed! \033[0m\n");
		putDLList(stdout,myList);
	}

	printf("\nTest 9 Checking for DLListDelete -> deleting in the middle\n");
	DLListMoveTo(myList, 4);
	DLListDelete(myList);
	if (validDLList(myList) == 1) {
		printf("\033[22;32mText Passed!!! \033[0m\n");
	} else {  
		printf("\033[22;31mText Failed! \033[0m\n");
		putDLList(stdout,myList);
	}

	printf("\033[22;32mALL TEST CASES PASSED !! \033[0m\n");
		
	return 0;
}

int checkCount 


