import { Calendar, Clock, CheckCircle, Target, Award, BookOpen } from "lucide-react";
import StatCard from "@/components/dashboard/StatCard";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const upcomingLessons = [
  { date: "27/12/2024", time: "14:00", instructor: "Carlos Mendes", type: "Prática" },
  { date: "28/12/2024", time: "10:00", instructor: "Carlos Mendes", type: "Prática" },
  { date: "30/12/2024", time: "08:00", instructor: "Carlos Mendes", type: "Prática" },
];

const completedLessons = [
  { date: "26/12/2024", time: "14:00", instructor: "Carlos Mendes", duration: "50 min", score: "Bom" },
  { date: "24/12/2024", time: "10:00", instructor: "Carlos Mendes", duration: "50 min", score: "Excelente" },
  { date: "22/12/2024", time: "08:00", instructor: "Carlos Mendes", duration: "50 min", score: "Bom" },
  { date: "20/12/2024", time: "14:00", instructor: "Carlos Mendes", duration: "50 min", score: "Regular" },
];

const Aluno = () => {
  const totalHours = 12;
  const requiredHours = 20;
  const progressPercentage = (totalHours / requiredHours) * 100;

  return (
    <div className="min-h-screen bg-background pt-20 pb-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8 animate-fade-in">
          <h1 className="text-3xl font-bold text-foreground mb-2">
            Bem-vindo, João! 🚗
          </h1>
          <p className="text-muted-foreground">
            Acompanhe seu progresso e próximas aulas
          </p>
        </div>

        {/* Progress Banner */}
        <div className="mb-8 rounded-2xl gradient-hero p-6 text-primary-foreground animate-fade-in" style={{ animationDelay: "0.1s" }}>
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold mb-1">Progresso para CNH - Categoria B</h2>
              <p className="text-primary-foreground/80">
                {totalHours} de {requiredHours} horas práticas obrigatórias completadas
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-3xl font-bold">{Math.round(progressPercentage)}%</p>
                <p className="text-sm text-primary-foreground/80">Completo</p>
              </div>
            </div>
          </div>
          <div className="mt-4">
            <div className="h-3 w-full rounded-full bg-primary-foreground/20">
              <div
                className="h-full rounded-full bg-primary-foreground transition-all duration-1000"
                style={{ width: `${progressPercentage}%` }}
              />
            </div>
            <div className="flex justify-between mt-2 text-sm text-primary-foreground/80">
              <span>0h</span>
              <span>20h (mínimo CONTRAN)</span>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <div className="animate-fade-in" style={{ animationDelay: "0.2s" }}>
            <StatCard
              title="Aulas Agendadas"
              value={3}
              subtitle="Próximos 7 dias"
              icon={Calendar}
              variant="primary"
            />
          </div>
          <div className="animate-fade-in" style={{ animationDelay: "0.3s" }}>
            <StatCard
              title="Horas Completadas"
              value={`${totalHours}h`}
              subtitle={`Faltam ${requiredHours - totalHours}h`}
              icon={Clock}
              variant="accent"
            />
          </div>
          <div className="animate-fade-in" style={{ animationDelay: "0.4s" }}>
            <StatCard
              title="Aulas Realizadas"
              value={14}
              subtitle="Total"
              icon={CheckCircle}
              variant="success"
            />
          </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
          {/* Upcoming Lessons */}
          <div className="lg:col-span-2 rounded-2xl border border-border bg-card p-6 shadow-card animate-fade-in" style={{ animationDelay: "0.6s" }}>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-bold text-foreground">Próximas Aulas</h2>
                <p className="text-sm text-muted-foreground">Suas aulas agendadas</p>
              </div>
              <Link to="/agendamento">
                <Button variant="default" size="sm" className="gradient-primary border-0">
                  Agendar Nova
                </Button>
              </Link>
            </div>

            <div className="space-y-4">
              {upcomingLessons.map((lesson, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between p-4 rounded-xl bg-secondary/50 border border-border"
                >
                  <div className="flex items-center gap-4">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl gradient-primary">
                      <Calendar className="h-5 w-5 text-primary-foreground" />
                    </div>
                    <div>
                      <p className="font-semibold text-foreground">{lesson.date}</p>
                      <p className="text-sm text-muted-foreground">
                        {lesson.time} • {lesson.instructor}
                      </p>
                    </div>
                  </div>
                  <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
                    {lesson.type}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Skills Progress */}
          <div className="rounded-2xl border border-border bg-card p-6 shadow-card animate-fade-in" style={{ animationDelay: "0.7s" }}>
            <div className="flex items-center gap-2 mb-6">
              <Award className="h-5 w-5 text-primary" />
              <h2 className="text-xl font-bold text-foreground">Habilidades</h2>
            </div>

            <div className="space-y-5">
              {skills.map((skill, i) => (
                <div key={i}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-foreground">{skill.name}</span>
                    <span className="text-xs text-muted-foreground">{skill.status}</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-secondary">
                    <div
                      className="h-full rounded-full gradient-primary transition-all duration-700"
                      style={{ width: `${skill.progress}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Lesson History */}
        <div className="rounded-2xl border border-border bg-card p-6 shadow-card animate-fade-in" style={{ animationDelay: "0.8s" }}>
          <div className="flex items-center gap-2 mb-6">
            <BookOpen className="h-5 w-5 text-primary" />
            <h2 className="text-xl font-bold text-foreground">Histórico de Aulas</h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Data</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Horário</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Instrutor</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Duração</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Avaliação</th>
                </tr>
              </thead>
              <tbody>
                {completedLessons.map((lesson, i) => (
                  <tr key={i} className="border-b border-border/50 last:border-0">
                    <td className="py-3 px-4 text-sm text-foreground">{lesson.date}</td>
                    <td className="py-3 px-4 text-sm text-foreground">{lesson.time}</td>
                    <td className="py-3 px-4 text-sm text-foreground">{lesson.instructor}</td>
                    <td className="py-3 px-4 text-sm text-foreground">{lesson.duration}</td>
                    <td className="py-3 px-4">
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-medium ${
                          lesson.score === "Excelente"
                            ? "bg-success/10 text-success"
                            : lesson.score === "Bom"
                            ? "bg-primary/10 text-primary"
                            : "bg-warning/10 text-warning"
                        }`}
                      >
                        {lesson.score}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Aluno;
