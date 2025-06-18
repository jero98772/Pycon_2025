import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Vector;
import java.util.List;
import java.util.ArrayList;


class CPU {
    private ROM rom;
    private RAM ram;
    private short registerD;
    private short registerA;
    ALU alu = new ALU();

    public CPU(ROM rom, RAM ram) {
        this.rom = rom;
        this.ram = ram;
    }

    // Method to execute a single instruction from ROM
    public String executeInstructions() {
        StringBuilder output = new StringBuilder();

        output.append("Number of ROM rows: ").append(rom.getNumRows()).append("\n");
        for (short instructionAddress = 0; instructionAddress < rom.getNumRows(); instructionAddress++) {
            Vector<Integer> instruction = rom.getValuesAt(instructionAddress);
            short typeInstruccion = instruction.get(0).shortValue(); 

            if (typeInstruccion == 1) { // C instruction
                short a = instruction.get(3).shortValue();   // a
                short zx = instruction.get(4).shortValue();  // c1
                short nx = instruction.get(5).shortValue();  // c2
                short zy = instruction.get(6).shortValue();  // c3
                short ny = instruction.get(7).shortValue();  // c4
                short f = instruction.get(8).shortValue();   // c5
                short no = instruction.get(9).shortValue();  // c6
                short d1 = instruction.get(10).shortValue();
                short d2 = instruction.get(11).shortValue();
                short d3 = instruction.get(12).shortValue();
                short j1 = instruction.get(13).shortValue();
                short j2 = instruction.get(14).shortValue();
                short j3 = instruction.get(15).shortValue();

                if (a == 0) { // register A
                    output.append("go register A\n");
                    this.alu.setInputs(this.registerD, this.registerA);
                } else { // memory
                    output.append("go memory\n");
                    this.alu.setInputs(this.registerD, this.ram.getValueAt(this.registerA));
                }
                this.alu.setControlBits(zx, nx, zy, ny, f, no);
                this.alu.compute();
                output.append("ALU\n");
                output.append(this.alu.getOut()).append("\n");
                this.handleRegisters(d1, d2, d3, this.alu.getOut());
                instructionAddress = this.jump(j1, j2, j3, this.alu.getOut(), instructionAddress);

            } else {
                // else is an instruction
                int intValue = binaryVectorToInt(instruction);
                this.registerA = (short) intValue;
            }

            output.append("registerA:\n");
            output.append(this.registerA).append("\n");
            output.append("registerD:\n");
            output.append(this.registerD).append("\n\n");
        }
        
        output.append("RAM First 20 Elements:\n");
        output.append(this.ram.getFirstElements(20));

        return output.toString();
    }

    public short jump(short j1, short j2, short j3, short out ,short romPosition) {
        if (j1 == 1 && j2 == 0 && j3 == 0 && out > 0) { // JGT
            romPosition = registerA;
        } else if (j1 == 1 && j2 == 0 && j3 == 1 && out == 0) { // JEQ
            romPosition = registerA;
        } else if (j1 == 1 && j2 == 0 && j3 == 1 && out >= 0) { // JGE
            romPosition = registerA;
        } else if (j1 == 0 && j2 == 1 && j3 == 0 && out < 0) { // JLT
            romPosition = registerA;
        } else if (j1 == 0 && j2 == 1 && j3 == 1 && out != 0) { // JNE
            romPosition = registerA;
        } else if (j1 == 0 && j2 == 1 && j3 == 1 && out <= 0) { // JLE
            romPosition = registerA;
        } else if (j1 == 1 && j2 == 1 && j3 == 1) { // JMP
            romPosition = registerA;
        } else {
            
        }
        return romPosition;
    }

    public void handleRegisters(short d1, short d2, short d3, short value) {

        if (d1 == 1) {
        System.out.println("registerA");
        System.out.println( value);
            this.registerA = value; // Store in A register
        }
        if (d2 == 1) {
            System.out.println("registerD");
            System.out.println( value);
            this.registerD = value; // Store in D register
        }
        if (d3 == 1) {
            System.out.println("ram");
            System.out.println( value);
            this.ram.setValueAt(value,this.registerA); // Store in RAM at address A
        }
    }
    private static int binaryVectorToInt(Vector<Integer> binaryVector) {
        int result = 0;
        int size = binaryVector.size();
        for (int i = 0; i < size; i++) {
            result |= (binaryVector.get(i) << (size - 1 - i));
        }
        return result;
    }
}
