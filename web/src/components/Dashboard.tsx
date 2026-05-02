import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Award, Target, BarChart3, Info } from 'lucide-react';
import { 
  type Course, 
  TranscriptProcessor, 
  OverallRating 
} from '../lib/gpa-engine';

interface DashboardProps {
  courses: Course[];
  programHours: number;
  nonGpaHours: number;
}

const BentoCard: React.FC<{
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactNode;
  className?: string;
  delay?: number;
  color?: 'accent' | 'emerald' | 'amber' | 'blue';
}> = ({ title, value, subtitle, icon, className, delay = 0, color = 'accent' }) => {
  const colorMap = {
    accent: 'text-accent',
    emerald: 'text-emerald-500',
    amber: 'text-amber-500',
    blue: 'text-blue-500',
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ delay, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className={`glass-card rounded-2xl p-8 relative group overflow-hidden ${className}`}
    >
      <div className="flex justify-between items-start mb-4">
        <div className={`p-3 bg-white/5 rounded-xl group-hover:scale-110 transition-transform duration-300 ${colorMap[color]}`}>
          {icon}
        </div>
      </div>
      <div>
        <h4 className="text-foreground-muted text-sm font-medium mb-1 tracking-wide uppercase">{title}</h4>
        <div className="text-4xl font-semibold text-gradient mb-2">{value}</div>
        {subtitle && <p className="text-foreground-subtle text-sm leading-relaxed">{subtitle}</p>}
      </div>
      
      {/* Background Glow */}
      <div className={`absolute -right-10 -bottom-10 w-40 h-40 rounded-full blur-[80px] opacity-10 group-hover:opacity-20 transition-opacity duration-500 ${
        color === 'accent' ? 'bg-accent' : 
        color === 'emerald' ? 'bg-emerald-500' : 
        color === 'amber' ? 'bg-amber-500' : 'bg-blue-500'
      }`} />
    </motion.div>
  );
};

export const Dashboard: React.FC<DashboardProps> = ({ courses, programHours, nonGpaHours }) => {
  const stats = useMemo(() => {
    const currentGpa = TranscriptProcessor.getCumulativeGpa(courses);
    const maxGpa = TranscriptProcessor.calculateMaxPossibleGpa(courses, programHours, nonGpaHours);
    const rating = TranscriptProcessor.calculateOverallRating(currentGpa);
    const maxRating = TranscriptProcessor.calculateOverallRating(maxGpa);
    const remainingHours = TranscriptProcessor.getRemainingHours(courses, programHours, nonGpaHours);
    
    return {
      currentGpa,
      maxGpa,
      rating,
      maxRating,
      remainingHours,
      completedCourses: courses.length
    };
  }, [courses, programHours, nonGpaHours]);

  const formatRating = (r: OverallRating) => r.replace('_', ' ').toUpperCase();

  return (
    <div className="container mx-auto px-6 pb-32">
      <div className="grid grid-cols-1 md:grid-cols-6 gap-6 auto-rows-[220px]">
        {/* Main GPA Card */}
        <BentoCard
          title="Current Cumulative GPA"
          value={stats.currentGpa.toFixed(2)}
          subtitle={`Based on ${stats.completedCourses} courses.`}
          icon={<BarChart3 className="w-6 h-6" />}
          className="md:col-span-4 md:row-span-1"
          color="accent"
        />

        {/* Rating Card */}
        <BentoCard
          title="Overall Rating"
          value={formatRating(stats.rating)}
          subtitle="Your current academic standing."
          icon={<Award className="w-6 h-6" />}
          className="md:col-span-2 md:row-span-1"
          color="blue"
          delay={0.1}
        />

        {/* Max GPA Card */}
        <BentoCard
          title="Maximum Possible GPA"
          value={stats.maxGpa.toFixed(2)}
          subtitle={`If you maintain a 4.0 for the remaining ${stats.remainingHours.toFixed(1)} hours.`}
          icon={<TrendingUp className="w-6 h-6" />}
          className="md:col-span-3 md:row-span-1"
          color="emerald"
          delay={0.2}
        />

        {/* Highest Rating Card */}
        <BentoCard
          title="Highest Achievable Rating"
          value={formatRating(stats.maxRating)}
          subtitle="The ceiling of your potential."
          icon={<Target className="w-6 h-6" />}
          className="md:col-span-3 md:row-span-1"
          color="amber"
          delay={0.3}
        />
        
        {/* Info Card */}
        <div className="md:col-span-6 glass-card rounded-2xl p-8 flex items-center gap-6">
           <div className="p-4 bg-white/5 rounded-2xl">
             <Info className="w-8 h-8 text-foreground-muted" />
           </div>
           <div>
             <h3 className="text-xl font-medium text-foreground mb-1">Deep Analysis Active</h3>
             <p className="text-foreground-muted">
               Using the Suez Canal University grading schema. All calculations are processed locally on your device for maximum privacy.
             </p>
           </div>
        </div>
      </div>
    </div>
  );
};
