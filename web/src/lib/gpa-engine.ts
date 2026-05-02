export enum LetterGrade {
  A_PLUS = "A+",
  A = "A",
  A_MINUS = "A-",
  B_PLUS = "B+",
  B = "B",
  B_MINUS = "B-",
  C_PLUS = "C+",
  C = "C",
  C_MINUS = "C-",
  D_PLUS = "D+",
  D = "D",
  D_MINUS = "D-",
  FAIL = "F",
  EXAM_FAIL = "BF",
  ABSENT = "Abs",
  PASS = "P",
}

export enum OverallRating {
  EXCELLENT = "excellent",
  VERY_GOOD = "very_good",
  GOOD = "good",
  ACCEPTED = "accepted",
  WEAK = "weak",
  TOO_WEAK = "too_weak",
}

export const RATING_THRESHOLDS: [number, OverallRating][] = [
  [3.5, OverallRating.EXCELLENT],
  [3.0, OverallRating.VERY_GOOD],
  [2.5, OverallRating.GOOD],
  [2.0, OverallRating.ACCEPTED],
  [1.0, OverallRating.WEAK],
  [0.0, OverallRating.TOO_WEAK],
];

export const GRADE_POINT_MAP: Record<string, number> = {
  [LetterGrade.A_PLUS]: 4.0,
  [LetterGrade.A]: 3.7,
  [LetterGrade.A_MINUS]: 3.4,
  [LetterGrade.B_PLUS]: 3.2,
  [LetterGrade.B]: 3.0,
  [LetterGrade.B_MINUS]: 2.8,
  [LetterGrade.C_PLUS]: 2.6,
  [LetterGrade.C]: 2.4,
  [LetterGrade.C_MINUS]: 2.2,
  [LetterGrade.D_PLUS]: 2.0,
  [LetterGrade.D]: 1.5,
  [LetterGrade.D_MINUS]: 1.0,
  [LetterGrade.FAIL]: 0.0,
  [LetterGrade.EXAM_FAIL]: 0.0,
  [LetterGrade.ABSENT]: 0.0,
};

export const ARABIC_TO_ENGLISH_GRADES: Record<string, LetterGrade> = {
  "أ+": LetterGrade.A_PLUS,
  "أ": LetterGrade.A,
  "أ-": LetterGrade.A_MINUS,
  "ب+": LetterGrade.B_PLUS,
  "ب": LetterGrade.B,
  "ب-": LetterGrade.B_MINUS,
  "ج+": LetterGrade.C_PLUS,
  "ج": LetterGrade.C,
  "ج-": LetterGrade.C_MINUS,
  "د+": LetterGrade.D_PLUS,
  "د": LetterGrade.D,
  "د-": LetterGrade.D_MINUS,
  "راسب": LetterGrade.FAIL,
  "BF": LetterGrade.EXAM_FAIL,
  "غائب": LetterGrade.ABSENT,
  "ناجح": LetterGrade.PASS,
};

export interface Course {
  code: string;
  name: string;
  credit_hours: number;
  degree: number;
  letter_grade: LetterGrade;
}

export class TranscriptProcessor {
  static getGpaPoints(letterGrade: LetterGrade): number | null {
    return GRADE_POINT_MAP[letterGrade] ?? null;
  }

  static getGradeQualityPoints(course: Course): number {
    return (this.getGpaPoints(course.letter_grade) ?? 0) * course.credit_hours;
  }

  static countsTowardGpa(course: Course): boolean {
    return course.letter_grade !== LetterGrade.PASS;
  }

  static getCumulativeGpa(courses: Course[]): number {
    const inGpaCourses = courses.filter(this.countsTowardGpa);
    const totalQualityPoints = inGpaCourses.reduce((sum, c) => sum + this.getGradeQualityPoints(c), 0);
    const totalHours = inGpaCourses.reduce((sum, c) => sum + c.credit_hours, 0);
    return totalHours > 0 ? totalQualityPoints / totalHours : 0;
  }

  static getRemainingHours(courses: Course[], programHours: number, nonGpaHours: number): number {
    const completedHours = courses.filter(this.countsTowardGpa).reduce((sum, c) => sum + c.credit_hours, 0);
    return Math.max(0, programHours - nonGpaHours - completedHours);
  }

  static calculateMaxPossibleGpa(courses: Course[], programHours: number, nonGpaHours: number): number {
    const remainingHours = this.getRemainingHours(courses, programHours, nonGpaHours);
    if (remainingHours <= 0) return this.getCumulativeGpa(courses);
    
    const inGpaCourses = courses.filter(this.countsTowardGpa);
    const currentQualityPoints = inGpaCourses.reduce((sum, c) => sum + this.getGradeQualityPoints(c), 0);
    const currentHours = inGpaCourses.reduce((sum, c) => sum + c.credit_hours, 0);
    
    const maxFutureQualityPoints = remainingHours * 4.0;
    return (currentQualityPoints + maxFutureQualityPoints) / (currentHours + remainingHours);
  }

  static calculateOverallRating(gpa: number): OverallRating {
    for (const [threshold, rating] of RATING_THRESHOLDS) {
      if (gpa >= threshold) return rating;
    }
    return OverallRating.TOO_WEAK;
  }

  static getRequiredAverageForRating(courses: Course[], targetRating: OverallRating, programHours: number, nonGpaHours: number): number | null {
    const targetThreshold = RATING_THRESHOLDS.find(([_, r]) => r === targetRating)?.[0] ?? 0;
    const inGpaCourses = courses.filter(this.countsTowardGpa);
    const currentQualityPoints = inGpaCourses.reduce((sum, c) => sum + this.getGradeQualityPoints(c), 0);
    const currentHours = inGpaCourses.reduce((sum, c) => sum + c.credit_hours, 0);
    const remainingHours = this.getRemainingHours(courses, programHours, nonGpaHours);

    if (remainingHours <= 0) return null;

    const requiredTotalQualityPoints = targetThreshold * (currentHours + remainingHours);
    const neededFromRemaining = requiredTotalQualityPoints - currentQualityPoints;
    return neededFromRemaining / remainingHours;
  }

  static predictFinalGpa(courses: Course[], hypotheticalGpa: number, programHours: number, nonGpaHours: number): number {
    const inGpaCourses = courses.filter(this.countsTowardGpa);
    const currentQualityPoints = inGpaCourses.reduce((sum, c) => sum + this.getGradeQualityPoints(c), 0);
    const currentHours = inGpaCourses.reduce((sum, c) => sum + c.credit_hours, 0);
    const remainingHours = this.getRemainingHours(courses, programHours, nonGpaHours);

    if (remainingHours <= 0) return this.getCumulativeGpa(courses);

    const totalQualityPoints = currentQualityPoints + (hypotheticalGpa * remainingHours);
    const totalHours = currentHours + remainingHours;
    return totalHours > 0 ? totalQualityPoints / totalHours : 0;
  }
}

export const parseTranscriptHtml = (htmlContent: string): Course[] => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlContent, 'text/html');
  const tables = Array.from(doc.querySelectorAll('table')).reverse();
  const allCourses: Course[] = [];

  const ARABIC_HEADERS = ["الكود", "الساعات المعتمدة", "الدرجة"];
  const ENGLISH_HEADERS = ["Code", "Credit Hours", "Grade"];
  const ARABIC_BOTTOM_KEYWORDS = ["المعدل الفصلى", "الساعات"];
  const ENGLISH_BOTTOM_KEYWORDS = ["Term GPA", "Attempted Hours"];

  tables.forEach(table => {
    const rows = Array.from(table.querySelectorAll('tr'));
    if (rows.length < 2) return;

    const headerText = rows[0].textContent || "";
    const isArabic = ARABIC_HEADERS.some(h => headerText.includes(h));
    const isEnglish = ENGLISH_HEADERS.some(h => headerText.includes(h));

    if (!isArabic && !isEnglish) return;

    rows.slice(1).forEach(row => {
      const cols = Array.from(row.querySelectorAll('td, th')).map(c => (c.textContent || "").trim());
      if (cols.length < 5) return;

      const firstCol = cols[0];
      const isBottomRow = isArabic 
        ? ARABIC_BOTTOM_KEYWORDS.some(k => firstCol.includes(k))
        : ENGLISH_BOTTOM_KEYWORDS.some(k => firstCol.includes(k));
      
      if (isBottomRow) return;

      const code = cols[0];
      const name = cols[1];
      const creditHours = parseFloat(cols[2].replace(',', '.'));
      const degree = parseFloat(cols[3]);
      const letterGradeStr = cols[4];

      if (isNaN(degree)) return;

      let letterGrade: LetterGrade;
      if (isArabic) {
        letterGrade = ARABIC_TO_ENGLISH_GRADES[letterGradeStr] || LetterGrade.FAIL;
      } else {
        letterGrade = letterGradeStr as LetterGrade;
      }

      allCourses.push({
        code,
        name,
        credit_hours: creditHours,
        degree,
        letter_grade: letterGrade
      });
    });
  });

  return allCourses;
};
