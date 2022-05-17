import java.io.*;
import java.util.*;

public class memSim {
    int TLB_SIZE = 16;
    int PAGE_SIZE = 256;

    public static void OPT(ArrayList<Integer> virtualAddys, int FRAMES) {}
    public static void LRU(ArrayList<Integer> virtualAddys, int FRAMES) {}

    // Uses FIFO page replacement algorithm
    public static void FIFO(ArrayList<Integer> virtualAddys, int FRAMES) {
        for (int i = 0; i < virtualAddys.size(); i++) {
            
        }
    }

    // Create list of virtual addresses based on text file
    public static ArrayList<Integer> getVirtualAddresses(Scanner file) {
        ArrayList<Integer> addys = new ArrayList<>();
        while (file.hasNextLine()) addys.add(Integer.parseInt(file.nextLine()));
        return addys;
    }

    // Checks to see if argument is a number or not
    public static boolean isNumeric(String arg) {
        try {
            Integer.parseInt(arg);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        Scanner file = new Scanner(new File(args[0]));
        int FRAMES = 256;
        String PRA = "FIFO";

        // Read in args and set FRAMES and PRA based on args
        if (args.length > 1) {
            for (int i = 1; i < args.length; i++) {
                if (isNumeric(args[i])) FRAMES = Integer.parseInt(args[i]);
                else PRA = args[i];
            }
        }

        // Read file and create list of virtual addresses
        ArrayList<Integer> virtualAddys = getVirtualAddresses(file);

        // Call each function according to PRA
        if (PRA.equals("OPT")) OPT(virtualAddys, FRAMES);
        else if (PRA.equals("LRU")) LRU(virtualAddys, FRAMES);
        else FIFO(virtualAddys, FRAMES);
    }
}
