#!/usr/bin/env wolframscript
(* ::Package:: *)

frequencies = {};
words = Import["words.txt"] //StringSplit;

SaveFrequency[word_]:= Module[{frequency},
(* Frequency is between 0 and 1 so this transformation is applied to have a more manageable number. The higher it is, the rarer the word is *)
frequency =-Log[WordFrequencyData[word, Language->"English"]]; 

If[NumericQ[frequency],
 AppendTo[frequencies, frequency], 
 AppendTo[frequencies, 23]]  (* Some rare words are not in Mathematica's database, so input a high number instead *)
];

Scan[SaveFrequency, words]; (* Append to frequencies each word frequency *)

Export["frequenciesTest.txt", frequencies]
