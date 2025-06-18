import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Vector;
import java.util.List;
import java.util.ArrayList;
// CPU class

// convert romvector of shorts  

class RAM {
    private short[] ram;

    public RAM(short size) {
        ram = new short[size];
    }

    // Method to set a value at a specific position
    public void setValueAt(short value, short position) {
        if (position >= 0 && position < ram.length) {
            ram[position] = value;
        } else {
            throw new IndexOutOfBoundsException("Invalid RAM position: " + position);
        }
    }

    // Method to get a value at a specific position
    public short getValueAt(short position) {
        if (position >= 0 && position < ram.length) {
            return ram[position];
        } else {
            throw new IndexOutOfBoundsException("Invalid RAM position: " + position);
        }
    }
    public void printFirstElements(int elementsToPrint) {

        for (int i = 0; i < elementsToPrint && i < ram.length; i++) {
            System.out.println(ram[i]);
        }
    }
}
