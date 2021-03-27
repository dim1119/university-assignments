
class ItemNode {

	public int item;
	public ItemNode next;

	public ItemNode(int item) {
		this.item = item;
		this.next = null;
	}
}

class ItemsList {
	private int nbNodes;
	private ItemNode first;
	private ItemNode last;

	public ItemsList() {
		this.first = null;
		this.last = null;
		this.nbNodes = 0;
	}

	public int size() { return nbNodes; }

	public boolean empty() { return first == null; }
	

	public boolean contains(ItemsList ilist) {
		
		//if either list is empty or if the ilist is bigger than the calling list it returns false
		
		if(empty() || ilist.empty() || ilist.size() > size()) {
			return false;
		}
		
		
		ItemNode current = first;

		
		//We need to compare two lists to each other, so we can check each item
		while(current.next!=null){

			ItemNode ilist_current = ilist.first;

			
			while(current.item != ilist_current.item) {

				//return false if the check reaches the end of the ilist

				
				if(ilist_current.next==null) {
					return false;
				} else {
					//else go to check the next node
					ilist_current = ilist_current.next;
				}
				
				
			}

			//go to the next node of the list calling the method and if it is the last return false

			if(current.next != null) {
				current = current.next; 
			} else {
				return false;
			}
			
		}

		//if all items are found return true
		return true;

	}
	
	
	public int append(int item) {
		
		ItemNode newNode = new ItemNode(item);

		// assign next node of the object to the first and then make the object first

		newNode.next = first;
		first = newNode;

		// after increasing the number of nodes return the number

		return ++nbNodes;
	}

	
	public void remove(ItemsList ilist) {
		
		//if the size of the calling is smaller than the size of ilist stop the method
		
		if(size()<ilist.size()) {
			System.out.println("You can't perform this action");
			return;
		}
		
		
		ItemNode ilist_current = ilist.first;
		
		//cycling through ilist's contents
		
		while (ilist_current.next != null) {

			// preparing variables to delete the node

			ItemNode current = first;
			ItemNode previous = first;

			// check all the items in the calling list for each item in ilist

			while (ilist_current.item != current.item) {
				if (current.next == null) {
					break;
				}
				current = current.next;
			}

			// remove the node by linking the one before to the one after

			if (current == first) {
				first = first.next;
			} else {
				previous.next = current.next;
			}

			// reduce nbNodes by 1
			nbNodes--;

			// go to the next ilist Node
			ilist_current = ilist_current.next;
		}
		
	}
}

class BuyerNode {

	public int id;
	public int value;
	public ItemsList itemsList;
	public BuyerNode next;


	public BuyerNode(int id, int value, ItemsList ilist) {
		this.id = id;
		this.value = value;
		this.itemsList = ilist;
	}
}

class BuyersList {
	public int opt;
	private int nbNodes;
	private BuyerNode first;
	private BuyerNode last;
	private static String whichFile; // keep track of files between methods
	private static boolean switchedFolder; // change the print output based on the folder
	private static BuyersList buyers = new BuyersList();

	public BuyersList() {
		this.first = null;
		this.last = null;
		this.nbNodes = 0;
	}

	public int readFile(String filename) {

		int m = 0;
		java.io.BufferedReader br = null;

		try {
			br = new java.io.BufferedReader(new java.io.FileReader(filename));

			// Read dimensions
			String line = br.readLine();
			String[] data = line.split(" ");
			// Number of items
			m = Integer.parseInt(data[0]);
			// Number of buyers
			int n = Integer.parseInt(data[1]);
			// Optimum revenue
			this.opt = Integer.parseInt(data[2]);

			// Read Buyers Information
			int id = 0;
			while((line = br.readLine()) != null) {
				data = line.split(" ");
				// Read value
				int value = Integer.parseInt(data[0]);
				// Read Item List
				ItemsList itemsList = new ItemsList();
				for(int i = 1; i < data.length; i++)
					itemsList.append(Integer.parseInt(data[i]));
				// Insert new buyer
				this.append(id++, value, itemsList);
			}
		} catch(java.io.IOException e) {
			e.printStackTrace();
		} finally {
			try { if (br != null) br.close(); }
			catch (java.io.IOException ex) { ex.printStackTrace(); }
		}
		return m;
	}

	public boolean empty() { return first == null; }

	public int size() { return nbNodes; }

	public int totalValue() {

		// first check if the List is empty making the value 0

		if (empty()) {
			return 0;
		}

		// go through every Buyer Node and add the value to totalValue

		BuyerNode current = first;
		int totalValue = 0;
		while (current.next != null) {

			totalValue += current.value;
			current = current.next;
		}

		return totalValue;
	}

	public int append(int id, int value, ItemsList ilist) {

		// creating a new BuyerNode and adding it to the list by making it first

		BuyerNode newNode = new BuyerNode(id, value, ilist);
		newNode.next = first;
		first = newNode;
		return ++nbNodes;
	}

	public BuyersList greedy(int m) {

		// read file from String whichFile and make a current BuyerNode
		buyers.readFile(whichFile);

		// create new BuyerNode object
		BuyerNode current = buyers.first;
		int count;
		int ratio = 0;
		int ratio2 = 0;
		BuyerNode tempNode;

		// cycle through every buyer
		for (count = 0; count < m; count++) {

			// calculate Ui/|Si|

			ratio = current.value / current.itemsList.size();

			// temporary BuyerNode object to check the rest of the list
			tempNode = buyers.first;

			while (tempNode != null) {

				// compare the ratio of the other Nodes in relation to object current
				ratio2 = tempNode.value / tempNode.itemsList.size();
				
				
				if (ratio > ratio2) {

					// try to remove the items that have smaller ratios then the item in current
					if (current.itemsList.contains(tempNode.itemsList)) {
						current.itemsList.remove(tempNode.itemsList);
					}		
				}
				
				tempNode = tempNode.next;
			}
			current = current.next;
		}
		return buyers;
	}
	

	private static void printReport(int m, int n, long avgtime, int greedy_value, int optTime) {
		
		//method to show the report for each file
		//the boolean switchedFolder is used to determine whether the n or the m is constant, which changes according to the folder
		if(!switchedFolder) {
			
			System.out.println("- n = " + n + " avgTime = " + avgtime + " greedy value = " + greedy_value + " opt value = " + optTime);
		}
		else {
			
			System.out.println("- m = " + m + " avgTime = " + avgtime + " greedy value = " + greedy_value + " opt value = " + optTime);
		}
	}
	
	private static long time10runner(int m) {
		
		
		// method that runs the algorithm 10 times and returns the average time to complete in milliseconds
		// using the built-in method nanoTime for more accurate results
		
		// store the current time in nanoseconds
		long startTimer = System.nanoTime(); 
		for(int i=0; i<10; i++) {
			buyers.greedy(m);
		}
		
		// store the time when the algorithm finishes 10 runs
		
		long stopTimer = System.nanoTime();
		
		// subtract the 2 values and get the execution time in nanoseconds, then return it in milliseconds
		
		long elapsedTime = stopTimer-startTimer;
		
		return elapsedTime/1000000;
		
		
		
	}
	public static void main(String[] args) {
		
		System.out.println("* m = 500");
		//m based output
		switchedFolder = false; 
		
		whichFile ="m500/p500x9000.txt";
		printReport(500, 9000, time10runner(500), buyers.size(), buyers.opt);
		
		
		whichFile ="m500/p500x7000.txt";
		printReport(500, 7000, time10runner(500), buyers.size(), buyers.opt);

		
		whichFile ="m500/p500x5000.txt";
		printReport(500, 5000, time10runner(500), buyers.size(), buyers.opt);
		
		
		whichFile ="m500/p500x3000.txt";
		printReport(500, 3000, time10runner(500), buyers.size(), buyers.opt);
		
		
		whichFile ="m500/p500x1000.txt";
		printReport(500, 1000, time10runner(500), buyers.size(), buyers.opt);
		
		
		
		
		// Running Files on n2000 folder
		//change to n based output, since now the n is constant
		
		System.out.println("* n = 2000");
		switchedFolder = true; 
		
		whichFile ="n2000/p1000x2000.txt";
		printReport(1000, 2000, time10runner(1000), buyers.size(), buyers.opt);
		
		
		whichFile ="n2000/p800x2000.txt";
		printReport(800, 2000, time10runner(800), buyers.size(), buyers.opt);
		
		
		whichFile ="n2000/p600x2000.txt";
		printReport(600, 2000, time10runner(600), buyers.size(), buyers.opt);

		
		whichFile ="n2000/p400x2000.txt";
		printReport(400, 2000, time10runner(400), buyers.size(), buyers.opt);
		
		
		whichFile ="n2000/p200x2000.txt";
		printReport(200, 2000, time10runner(200), buyers.size(), buyers.opt);
		
		

		
		
		
	}

	
}

