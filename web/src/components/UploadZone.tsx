import React, { useCallback, useState } from 'react';
import { Upload, CheckCircle, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface UploadZoneProps {
  onUpload: (content: string, fileName: string) => void;
  programHours: number;
  setProgramHours: (v: number) => void;
  nonGpaHours: number;
  setNonGpaHours: (v: number) => void;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ 
  onUpload, 
  programHours, 
  setProgramHours, 
  nonGpaHours, 
  setNonGpaHours 
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [fileName, setFileName] = useState('');

  const handleFile = async (file: File) => {
    if (file.type !== 'text/html' && !file.name.endsWith('.html')) {
      setStatus('error');
      return;
    }

    try {
      const content = await file.text();
      setFileName(file.name);
      setStatus('success');
      onUpload(content, file.name);
    } catch (err) {
      setStatus('error');
    }
  };

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, []);

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  return (
    <div id="upload-section" className="w-full px-6 mb-24">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <motion.div
          id="drop-zone"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={onDrop}
          className={cn(
            "lg:col-span-2 relative group glass-card rounded-2xl p-8 border-2 border-dashed transition-all duration-300 text-center cursor-pointer overflow-hidden min-h-[200px] flex flex-col justify-center",
            isDragging ? "border-accent bg-accent/5 scale-[1.01]" : "border-white/10 hover:border-white/20",
            status === 'success' && "border-emerald-500/50 bg-emerald-500/5",
            status === 'error' && "border-red-500/50 bg-red-500/5"
          )}
        >
          <input
            id="file-input"
            type="file"
            accept=".html"
            className="absolute inset-0 opacity-0 cursor-pointer"
            onChange={onFileChange}
          />
          
          <AnimatePresence mode="wait">
            {status === 'idle' && (
              <motion.div
                key="idle"
                id="upload-status-idle"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex items-center gap-6 justify-center"
              >
                <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <Upload className="w-6 h-6 text-foreground-muted group-hover:text-accent" />
                </div>
                <div className="text-left">
                  <h3 id="upload-idle-heading" className="text-lg font-medium text-foreground">Upload Transcript</h3>
                  <p className="text-foreground-muted text-xs">
                    Drop your <span className="text-foreground font-mono">MyU.html</span> here or click to browse
                  </p>
                </div>
              </motion.div>
            )}

            {status === 'success' && (
              <motion.div
                key="success"
                id="upload-status-success"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="flex items-center gap-6 justify-center"
              >
                <div className="w-12 h-12 bg-emerald-500/10 rounded-xl flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-emerald-500" />
                </div>
                <div className="text-left">
                  <h3 id="upload-success-heading" className="text-lg font-medium text-foreground">File Ready</h3>
                  <p id="upload-success-filename" className="text-emerald-500/80 text-xs font-mono">{fileName}</p>
                </div>
              </motion.div>
            )}

            {status === 'error' && (
              <motion.div
                key="error"
                id="upload-status-error"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="flex items-center gap-6 justify-center"
              >
                <div className="w-12 h-12 bg-red-500/10 rounded-xl flex items-center justify-center">
                  <AlertCircle className="w-6 h-6 text-red-500" />
                </div>
                <div className="text-left">
                  <h3 id="upload-error-heading" className="text-lg font-medium text-foreground">Invalid File</h3>
                  <p id="upload-error-message" className="text-red-500/80 text-xs">Please upload an HTML file.</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out pointer-events-none" />
        </motion.div>

        {/* Settings Panel */}
        <motion.div
          id="settings-panel"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="glass-card rounded-2xl p-8 space-y-6"
        >
          <div>
            <label id="program-hours-label" className="text-xs font-mono uppercase tracking-widest text-foreground-subtle block mb-3">Program Hours</label>
            <div className="relative group">
              <input
                id="program-hours-input"
                type="number" 
                value={programHours}
                onChange={(e) => setProgramHours(parseFloat(e.target.value) || 0)}
                className="w-full bg-[#0F0F12] border border-white/10 rounded-lg px-4 py-3 text-foreground focus:outline-none focus:border-accent transition-colors"
              />
              <div className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground-subtle text-xs">Hrs</div>
            </div>
          </div>

          <div>
            <label id="non-gpa-hours-label" className="text-xs font-mono uppercase tracking-widest text-foreground-subtle block mb-3">Non GPA Hours</label>
            <div className="relative group">
              <input
                id="non-gpa-hours-input"
                type="number" 
                value={nonGpaHours}
                onChange={(e) => setNonGpaHours(parseFloat(e.target.value) || 0)}
                className="w-full bg-[#0F0F12] border border-white/10 rounded-lg px-4 py-3 text-foreground focus:outline-none focus:border-accent transition-colors"
              />
              <div className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground-subtle text-xs">Hrs</div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};
