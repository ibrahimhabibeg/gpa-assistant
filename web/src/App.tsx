import { useState } from 'react';
import { Hero } from './components/Hero';
import { AmbientBackground } from './components/AmbientBackground';
import { Steps } from './components/Steps';
import { UploadZone } from './components/UploadZone';
import { Dashboard } from './components/Dashboard';
import { Questions } from './components/Questions';
import { ProjectInfo } from './components/ProjectInfo';
import { parseTranscriptHtml, type Course } from './lib/gpa-engine';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [hasData, setHasData] = useState(false);
  
  // Program requirements state
  const [programHours, setProgramHours] = useState(143);
  const [nonGpaHours, setNonGpaHours] = useState(9);

  const handleUpload = (content: string) => {
    const parsedCourses = parseTranscriptHtml(content);
    setCourses(parsedCourses);
    setHasData(true);
    
    // Scroll to dashboard after short delay
    setTimeout(() => {
      window.scrollTo({
        top: window.innerHeight * 0.8,
        behavior: 'smooth'
      });
    }, 500);
  };

  return (
    <div className="relative min-h-screen selection:bg-accent/30">
      <AmbientBackground />
      
      <main className="container mx-auto">
        <Hero />
        
        <ProjectInfo />
        
        <Steps />
        
        <UploadZone 
          onUpload={handleUpload}
          programHours={programHours}
          setProgramHours={setProgramHours}
          nonGpaHours={nonGpaHours}
          setNonGpaHours={setNonGpaHours}
        />

        <AnimatePresence>
          {hasData && (
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            >
              <Dashboard 
                courses={courses} 
                programHours={programHours} 
                nonGpaHours={nonGpaHours} 
              />
              <Questions 
                courses={courses} 
                programHours={programHours} 
                nonGpaHours={nonGpaHours} 
              />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer className="py-20 border-t border-white/[0.06] mt-20 relative z-10">
        <div className="container mx-auto px-6 text-center">
          <p className="text-foreground-muted text-sm mb-4">
            Built with precision for Suez Canal University Students.
          </p>
          <div className="flex justify-center gap-6 text-xs font-mono uppercase tracking-widest text-foreground-subtle">
            <span>Open Source</span>
            <span>Privacy First</span>
            <span>No Cookies</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
