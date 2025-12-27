import { Clock, MapPin, User, Car } from "lucide-react";
import { cn } from "@/lib/utils";

interface LessonCardProps {
  studentName: string;
  date: string;
  time: string;
  duration: string;
  location: string;
  vehicleType: string;
  status: "scheduled" | "in-progress" | "completed" | "cancelled";
  lessonNumber: number;
  totalLessons: number;
}

const LessonCard = ({
  studentName,
  date,
  time,
  duration,
  location,
  vehicleType,
  status,
  lessonNumber,
  totalLessons,
}: LessonCardProps) => {
  const statusConfig = {
    scheduled: {
      label: "Agendada",
      className: "bg-primary/10 text-primary border-primary/20",
    },
    "in-progress": {
      label: "Em andamento",
      className: "bg-warning/10 text-warning border-warning/20",
    },
    completed: {
      label: "Concluída",
      className: "bg-success/10 text-success border-success/20",
    },
    cancelled: {
      label: "Cancelada",
      className: "bg-destructive/10 text-destructive border-destructive/20",
    },
  };

  const { label, className: statusClassName } = statusConfig[status];

  return (
    <div className="group relative overflow-hidden rounded-2xl border border-border bg-card p-5 shadow-card transition-all duration-300 hover:shadow-card-hover hover:-translate-y-1">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-secondary">
            <User className="h-6 w-6 text-foreground" />
          </div>
          <div>
            <h3 className="font-semibold text-foreground">{studentName}</h3>
            <p className="text-sm text-muted-foreground">
              Aula {lessonNumber} de {totalLessons}
            </p>
          </div>
        </div>
        <span
          className={cn(
            "rounded-full border px-3 py-1 text-xs font-medium",
            statusClassName
          )}
        >
          {label}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Clock className="h-4 w-4" />
          <span>
            {date} às {time}
          </span>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span className="font-medium text-foreground">{duration}</span>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <MapPin className="h-4 w-4" />
          <span>{location}</span>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Car className="h-4 w-4" />
          <span>{vehicleType}</span>
        </div>
      </div>

      {/* Progress indicator */}
      <div className="mt-4 pt-4 border-t border-border">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-muted-foreground">Progresso do aluno</span>
          <span className="text-xs font-medium text-foreground">
            {Math.round((lessonNumber / totalLessons) * 100)}%
          </span>
        </div>
        <div className="h-2 w-full rounded-full bg-secondary">
          <div
            className="h-full rounded-full gradient-primary transition-all duration-500"
            style={{ width: `${(lessonNumber / totalLessons) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default LessonCard;
