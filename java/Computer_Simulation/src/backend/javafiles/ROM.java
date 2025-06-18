import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Vector;
import java.util.List;
import java.util.ArrayList;
public class ROM {
    private Vector<Vector<Integer>> rom;

    public ROM(int rows, int columns) {
        rom = new Vector<>(rows);
        for (int i = 0; i < rows; i++) {
            rom.add(new Vector<>(columns));
            for (int j = 0; j < columns; j++) {
                rom.get(i).add(0); // Initialize with zeros
            }
        }
    }

    // Method to load ROM from a text file
    public void loadRomFromFile(String fileName) {
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line;
            int rowIndex = 0;

            while ((line = br.readLine()) != null && rowIndex < rom.size()) {
                // Ensure the line is not longer than the number of columns in rom
                if (line.length() > rom.get(rowIndex).size()) {
                    line = line.substring(0, rom.get(rowIndex).size());
                }

                for (int colIndex = 0; colIndex < line.length() && colIndex < rom.get(rowIndex).size(); colIndex++) {
                    // Convert each character to an integer
                    int value = Character.getNumericValue(line.charAt(colIndex));
                    rom.get(rowIndex).set(colIndex, value);
                }
                rowIndex++;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Method to get the values at a specific position
    public Vector<Integer> getValuesAt(int position) {
        if (position >= 0 && position < rom.size()) {
            return rom.get(position);
        } else {
            throw new IndexOutOfBoundsException("Invalid ROM position: " + position);
        }
    }
    public static List<Short> convertShortToBitVector(short value) {
        List<Short> bitVector = new ArrayList<>(16);
        
        for (int i = 0; i < 16; i++) {
            // Shift right and mask with 1 to get the bit at position i
            bitVector.add(0, (short)((value >> i) & 1));
        }
        
        return bitVector;
    }    // Method to get the number of rows
    public int getNumRows() {
        return rom.size();
    }


}
