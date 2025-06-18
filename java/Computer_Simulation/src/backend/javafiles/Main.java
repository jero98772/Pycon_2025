import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Vector;
import java.util.List;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        // Initialize ROM and RAM
        
        ROM rom = new ROM(8, 16);
        short sizeram = 32767;
        RAM ram = new RAM(sizeram );


        rom.loadRomFromFile("rom.txt");

        // Create CPU with ROM and RAM
        CPU cpu = new CPU(rom, ram);

        // Execute instructions
        cpu.executeInstructions();
        System.out.print("finish");
    }
}
