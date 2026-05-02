import React from 'react';
import { Users, BookOpen, Github as GithubIcon, ExternalLink } from 'lucide-react';
import { motion } from 'framer-motion';

export const ProjectInfo: React.FC = () => {
  const team = [
    "Ibrahim Habib",
    "Zeyad Mohamed",
    "Youssef Ahmed",
    "Youssef Mahmoud",
    "Mohamed Essam"
  ];

  const courseDetails = [
    { label: "Instructor", value: "Dr. Mohamed Mead" },
    { label: "Teaching Assistant", value: "Eng. Merhan Hisham" },
    { label: "Course", value: "Software Requirements Engineering (SEN 302)" },
    { label: "Program", value: "Software Engineering, Suez Canal University" },
    { label: "Semester", value: "Spring 2026" }
  ];

  return (
    <section className="container mx-auto px-6 py-24 border-t border-white/[0.06]">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Team Section */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="glass-card rounded-2xl p-8"
        >
          <div className="flex items-center gap-3 mb-8">
            <div className="p-2 bg-accent/10 rounded-lg">
              <Users className="w-5 h-5 text-accent" />
            </div>
            <h3 className="text-xl font-semibold text-gradient">Project Team</h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {team.map((member, i) => (
              <div key={i} className="flex items-center gap-3 text-foreground-muted hover:text-foreground transition-colors group">
                <div className="w-1.5 h-1.5 rounded-full bg-accent/40 group-hover:bg-accent transition-colors" />
                <span className="text-sm font-medium">{member}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Course Info Section */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="glass-card rounded-2xl p-8"
        >
          <div className="flex items-center gap-3 mb-8">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <BookOpen className="w-5 h-5 text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-gradient">Course Information</h3>
          </div>
          <div className="space-y-4">
            {courseDetails.map((detail, i) => (
              <div key={i} className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-1 border-b border-white/[0.04] pb-3 last:border-0 last:pb-0">
                <span className="text-xs font-mono uppercase tracking-widest text-foreground-subtle">{detail.label}</span>
                <span className="text-sm font-medium text-foreground-muted">{detail.value}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* GitHub Link */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.2, duration: 0.8 }}
        className="mt-12 flex justify-center"
      >
        <a 
          href="https://github.com/ibrahimhabibeg/gpa-assistant" 
          target="_blank" 
          rel="noopener noreferrer"
          className="group flex items-center gap-3 px-6 py-3 bg-white/5 hover:bg-white/10 rounded-full border border-white/10 transition-all duration-300 hover:scale-105"
        >
          <GithubIcon className="w-5 h-5 text-foreground-muted group-hover:text-foreground transition-colors" />
          <span className="text-sm font-medium text-foreground-muted group-hover:text-foreground transition-colors">
            View Source on GitHub
          </span>
          <ExternalLink className="w-4 h-4 text-foreground-subtle group-hover:text-accent transition-colors" />
        </a>
      </motion.div>
    </section>
  );
};
