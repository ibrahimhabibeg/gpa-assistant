import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HelpCircle, ChevronRight, Calculator, Target, TrendingUp } from 'lucide-react';
import { 
  type Course, 
  TranscriptProcessor, 
  OverallRating,
  RATING_THRESHOLDS 
} from '../lib/gpa-engine';

interface QuestionsProps {
  courses: Course[];
  programHours: number;
  nonGpaHours: number;
}

const QUESTION_CAN_REACH = "Can I still reach a specific rating?";
const QUESTION_REQUIRED_AVERAGE = "What average GPA do I need for a target rating?";
const QUESTION_HYPOTHETICAL = "What will my final GPA be if I maintain a specific GPA?";

export const Questions: React.FC<QuestionsProps> = ({ courses, programHours, nonGpaHours }) => {
  const [selectedQuestion, setSelectedQuestion] = useState(QUESTION_CAN_REACH);
  const [targetRating, setTargetRating] = useState<OverallRating>(OverallRating.EXCELLENT);
  const [hypotheticalGpa, setHypotheticalGpa] = useState(3.5);

  const answer = useMemo(() => {
    if (selectedQuestion === QUESTION_CAN_REACH) {
      const maxGpa = TranscriptProcessor.calculateMaxPossibleGpa(courses, programHours, nonGpaHours);
      const threshold = RATING_THRESHOLDS.find(([_, r]) => r === targetRating)?.[0] ?? 0;
      return maxGpa >= threshold ? "Yes, this rating is still achievable!" : "Unfortunately, this rating is no longer reachable.";
    }
    
    if (selectedQuestion === QUESTION_REQUIRED_AVERAGE) {
      const req = TranscriptProcessor.getRequiredAverageForRating(courses, targetRating, programHours, nonGpaHours);
      if (req === null) return "N/A";
      if (req > 4.0) return `Impossible (Requires ${req.toFixed(2)} GPA)`;
      if (req < 0) return "You've already achieved this target!";
      return `You need an average of ${req.toFixed(2)} in your remaining courses.`;
    }

    if (selectedQuestion === QUESTION_HYPOTHETICAL) {
      const predicted = TranscriptProcessor.predictFinalGpa(courses, hypotheticalGpa, programHours, nonGpaHours);
      return `Your predicted final GPA would be ${predicted.toFixed(2)}.`;
    }

    return "";
  }, [selectedQuestion, targetRating, hypotheticalGpa, courses, programHours, nonGpaHours]);

  return (
    <section className="container mx-auto px-6 py-20">
      <div className="flex items-center gap-3 mb-10">
        <div className="p-2 bg-accent/10 rounded-lg">
          <HelpCircle className="w-5 h-5 text-accent" />
        </div>
        <h2 className="text-2xl font-semibold text-gradient">Ask a Question</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Sidebar / Question Selection */}
        <div className="lg:col-span-1 space-y-3">
          {[QUESTION_CAN_REACH, QUESTION_REQUIRED_AVERAGE, QUESTION_HYPOTHETICAL].map((q) => (
            <button
              key={q}
              onClick={() => setSelectedQuestion(q)}
              className={`w-full text-left p-4 rounded-xl border transition-all duration-300 flex items-center justify-between group ${
                selectedQuestion === q 
                ? "bg-accent/10 border-accent/30 text-foreground" 
                : "bg-white/5 border-white/5 text-foreground-muted hover:bg-white/8"
              }`}
            >
              <span className="text-sm font-medium">{q}</span>
              <ChevronRight className={`w-4 h-4 transition-transform ${selectedQuestion === q ? "translate-x-0 opacity-100" : "-translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100"}`} />
            </button>
          ))}
        </div>

        {/* Interaction & Answer Area */}
        <div className="lg:col-span-2 glass-card rounded-2xl p-8 min-h-[300px] flex flex-col">
          <div className="flex-1">
            <AnimatePresence mode="wait">
              <motion.div
                key={selectedQuestion}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="space-y-8"
              >
                {selectedQuestion === QUESTION_CAN_REACH || selectedQuestion === QUESTION_REQUIRED_AVERAGE ? (
                  <div className="space-y-4">
                    <label className="text-xs font-mono uppercase tracking-widest text-foreground-subtle">Target Rating</label>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                      {RATING_THRESHOLDS.map(([_, r]) => (
                        <button
                          key={r}
                          onClick={() => setTargetRating(r)}
                          className={`px-4 py-2 rounded-lg text-xs font-medium border transition-all ${
                            targetRating === r 
                            ? "bg-accent border-accent text-white shadow-[0_0_15px_rgba(94,106,210,0.4)]" 
                            : "bg-white/5 border-white/10 text-foreground-muted hover:border-white/20"
                          }`}
                        >
                          {r.replace('_', ' ').toUpperCase()}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <label className="text-xs font-mono uppercase tracking-widest text-foreground-subtle">Hypothetical GPA</label>
                      <span className="text-accent font-semibold">{hypotheticalGpa.toFixed(2)}</span>
                    </div>
                    <input 
                      type="range" 
                      min="0" 
                      max="4" 
                      step="0.05" 
                      value={hypotheticalGpa}
                      onChange={(e) => setHypotheticalGpa(parseFloat(e.target.value))}
                      className="w-full accent-accent h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="flex justify-between text-[10px] font-mono text-foreground-subtle uppercase tracking-tighter">
                      <span>0.00</span>
                      <span>2.00</span>
                      <span>4.00</span>
                    </div>
                  </div>
                )}
              </motion.div>
            </AnimatePresence>
          </div>

          <div className="mt-8 pt-8 border-t border-white/5">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center text-accent">
                {selectedQuestion === QUESTION_HYPOTHETICAL ? <TrendingUp className="w-6 h-6" /> : <Target className="w-6 h-6" />}
              </div>
              <div>
                <h4 className="text-xs font-mono uppercase tracking-widest text-foreground-subtle mb-1">Analysis Result</h4>
                <p className="text-xl font-medium text-foreground">{answer}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
