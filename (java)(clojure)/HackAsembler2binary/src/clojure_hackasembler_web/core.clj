(ns clojure_hackasembler_web.core
  (:require [clojure.string :as str]
            [clojure.tools.cli :refer [parse-opts]]
            [clojure.java.io :as io])
  (:gen-class))

;; Predefined symbols
(def predefined-symbols
  {"R0" 0, "R1" 1, "R2" 2, "R3" 3, "R4" 4, "R5" 5, "R6" 6, "R7" 7,
   "R8" 8, "R9" 9, "R10" 10, "R11" 11, "R12" 12, "R13" 13, "R14" 14, "R15" 15
   "SP" 0, "LCL" 1, "ARG" 2, "THIS" 3, "THAT" 4
   "SCREEN" 16384, "KBD" 24576})

;; Computation codes
(def comp-codes
  {"0" "0101010", "1" "0111111", "-1" "0111010"
   "D" "0001100", "A" "0110000", "!D" "0001101", "!A" "0110001"
   "-D" "0001111", "-A" "0110011", "D+1" "0011111", "A+1" "0110111"
   "D-1" "0001110", "A-1" "0110010", "D+A" "0000010", "D-A" "0010011"
   "A-D" "0000111", "D&A" "0000000", "D|A" "0010101"
   "M" "1110000", "!M" "1110001", "-M" "1110011", "M+1" "1110111"
   "M-1" "1110010", "D+M" "1000010", "D-M" "1010011", "M-D" "1000111"
   "D&M" "1000000", "D|M" "1010101"})

;; Destination codes
(def dest-codes
  {"" "000", "M" "001", "D" "010", "MD" "011"
   "A" "100", "AM" "101", "AD" "110", "AMD" "111"})

;; Jump codes
(def jump-codes
  {"" "000", "JGT" "001", "JEQ" "010", "JGE" "011"
   "JLT" "100", "JNE" "101", "JLE" "110", "JMP" "111"})

(defn clean-line
  "Remove comments and whitespace from a line"
  [line]
  (-> line
      (str/split #"//")
      first
      str/trim))

(defn label?
  "Check if a line is a label"
  [line]
  (and (str/starts-with? line "(")
       (str/ends-with? line ")")))

(defn numeric?
  "Check if a string represents a number"
  [s]
  (try
    (Integer/parseInt s)
    true
    (catch NumberFormatException _ false)))

(defn first-pass
  "First pass: collect labels and their addresses"
  [lines]
  (loop [lines lines
         instruction-address 0
         symbol-table predefined-symbols]
    (if (empty? lines)
      symbol-table
      (let [line (clean-line (first lines))]
        (cond
          (empty? line)
          (recur (rest lines) instruction-address symbol-table)
          
          (label? line)
          (let [label (subs line 1 (dec (count line)))]
            (recur (rest lines) 
                   instruction-address 
                   (assoc symbol-table label instruction-address)))
          
          :else
          (recur (rest lines) (inc instruction-address) symbol-table))))))

(defn translate-a-instruction
  "Translate A-instruction to binary"
  [instruction symbol-table next-var-addr]
  (let [symbol (subs instruction 1)] ; Remove @
    (cond
      (numeric? symbol)
      (let [address (Integer/parseInt symbol)]
        [symbol-table next-var-addr (format "0%015d" (Long/parseLong (Integer/toBinaryString address)))])
      
      (contains? symbol-table symbol)
      (let [address (symbol-table symbol)]
        [symbol-table next-var-addr (format "0%015d" (Long/parseLong (Integer/toBinaryString address)))])
      
      :else
      (let [address next-var-addr
            new-symbol-table (assoc symbol-table symbol address)]
        [new-symbol-table (inc next-var-addr) (format "0%015d" (Long/parseLong (Integer/toBinaryString address)))]))))

(defn parse-c-instruction
  "Parse C-instruction into dest, comp, and jump parts"
  [instruction]
  (let [has-equals? (str/includes? instruction "=")
        has-semicolon? (str/includes? instruction ";")]
    (cond
      (and has-equals? has-semicolon?)
      (let [[dest rest] (str/split instruction #"=" 2)
            [comp jump] (str/split rest #";" 2)]
        [dest comp jump])
      
      has-equals?
      (let [[dest comp] (str/split instruction #"=" 2)]
        [dest comp ""])
      
      has-semicolon?
      (let [[comp jump] (str/split instruction #";" 2)]
        ["" comp jump])
      
      :else
      ["" instruction ""])))

(defn translate-c-instruction
  "Translate C-instruction to binary"
  [instruction]
  (let [[dest comp jump] (parse-c-instruction instruction)
        dest-code (dest-codes dest)
        comp-code (comp-codes comp)
        jump-code (jump-codes jump)]
    (when (or (nil? dest-code) (nil? comp-code) (nil? jump-code))
      (throw (IllegalArgumentException. (str "Invalid C-instruction: " instruction))))
    (str "111" comp-code dest-code jump-code)))

(defn translate-instruction
  "Translate a single instruction to binary"
  [instruction symbol-table next-var-addr]
  (if (str/starts-with? instruction "@")
    (translate-a-instruction instruction symbol-table next-var-addr)
    [symbol-table next-var-addr (translate-c-instruction instruction)]))

(defn second-pass
  "Second pass: generate machine code"
  [lines symbol-table]
  (loop [lines lines
         symbol-table symbol-table
         next-var-addr 16
         result []]
    (if (empty? lines)
      (str/join "\n" result)
      (let [line (clean-line (first lines))]
        (cond
          (or (empty? line) (label? line))
          (recur (rest lines) symbol-table next-var-addr result)
          
          :else
          (let [[new-symbol-table new-next-var-addr binary-instruction]
                (translate-instruction line symbol-table next-var-addr)]
            (recur (rest lines) 
                   new-symbol-table 
                   new-next-var-addr
                   (conj result binary-instruction))))))))

(defn assemble
  "Assemble assembly code to binary"
  [assembly-code]
  (let [lines (str/split-lines assembly-code)
        symbol-table (first-pass lines)]
    (second-pass lines symbol-table)))

(defn assemble-file
  "Assemble a file"
  [input-file output-file]
  (let [assembly-code (slurp input-file)
        binary-code (assemble assembly-code)]
    (spit output-file binary-code)))

(def cli-options
  [["-h" "--help" "Show help"]])

(defn usage [options-summary]
  (->> ["Hack Assembler - Convert Hack assembly language to binary"
        ""
        "Usage: lein run [options] input.asm [output.hack]"
        ""
        "Options:"
        options-summary
        ""
        "If output file is not specified, output will be printed to stdout"]
       (str/join \newline)))
(comment
(defn demo-mode []
  (let [test-code "// Simple program to add two numbers
@2
D=A
@3
D=D+A
@0
M=D
// Loop example
@i
M=1
(LOOP)
@i
D=M
@100
D=D-A
@END
D;JGT
@i
M=M+1
@LOOP
0;JMP
(END)
@END
0;JMP"
        binary-code (assemble test-code)]
    (println "=== DEMO MODE ===")
    (println "Assembly Code:")
    (println test-code)
    (println "\nBinary Code:")
    (println binary-code)
    (println "\n=== USAGE ===")
    (println "To assemble your own files:")
    (println "lein run yourfile.asm")
    (println "lein run input.asm output.hack")))

(defn -main [& args]
  (let [{:keys [options arguments summary]} (parse-opts args cli-options)]
    (cond
      (:help options)
      (println (usage summary))
      
      (empty? arguments)
      (demo-mode)
      
      (= 1 (count arguments))
      (let [input-file (first arguments)]
        (if (.exists (io/file input-file))
          (println (assemble (slurp input-file)))
          (println "Error: Input file does not exist:" input-file)))
      
      (= 2 (count arguments))
      (let [[input-file output-file] arguments]
        (if (.exists (io/file input-file))
          (do
            (assemble-file input-file output-file)
            (println "Assembly complete. Output written to:" output-file))
          (println "Error: Input file does not exist:" input-file)))
      
      :else
      (println (usage summary)))))
)