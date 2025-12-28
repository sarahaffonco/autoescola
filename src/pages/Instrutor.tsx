import { Calendar, Users, CheckCircle, Clock, TrendingUp, AlertCircle } from "lucide-react";
import StatCard from "@/components/dashboard/StatCard";
import LessonCard from "@/components/dashboard/LessonCard";

const mockLessons = [
  {
    studentName: "Maria Silva",
    date: "27/12/2024",
    time: "08:00",
    duration: "50 min",
    location: "Centro",
    vehicleType: "Categoria B",
    status: "scheduled" as const,
    lessonNumber: 12,
    totalLessons: 20,
  },
  {
    studentName: "João Santos",
    date: "27/12/2024",
    time: "09:00",
    duration: "50 min",
    location: "Zona Sul",
    vehicleType: "Categoria B",
    status: "in-progress" as const,
    lessonNumber: 8,
    totalLessons: 20,
  },
  {
    studentName: "Ana Costa",
    date: "27/12/2024",
    time: "10:00",
    duration: "50 min",
    location: "Centro",
    vehicleType: "Categoria A",
    status: "scheduled" as const,
    lessonNumber: 15,
    totalLessons: 20,
  },
  {
    studentName: "Pedro Oliveira",
    date: "26/12/2024",
    time: "14:00",
    duration: "50 min",
    location: "Zona Norte",
    vehicleType: "Categoria B",
    status: "completed" as const,
    lessonNumber: 20,
    totalLessons: 20,
  },
];

const Instrutor = () => {
  return (
    <div className="min-h-screen bg-background pt-20 pb-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8 animate-fade-in">
          <h1 className="text-3xl font-bold text-foreground mb-2">
            Olá, Instrutor Carlos! 👋
          </h1>
          <p className="text-muted-foreground">
            Confira suas aulas e métricas do dia
          </p>
        </div>

        {/* Alert Banner */}
        <div className="mb-8 rounded-2xl gradient-primary p-4 flex items-center gap-4 animate-fade-in" style={{ animationDelay: "0.1s" }}>
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-foreground/20">
            <AlertCircle className="h-5 w-5 text-primary-foreground" />
          </div>
          <div>
            <p className="font-medium text-primary-foreground">
              Lembrete: Nova resolução CONTRAN 168/2004
            </p>
            <p className="text-sm text-primary-foreground/80">
              Mínimo de 20 horas de aulas práticas obrigatórias para todos os alunos
            </p>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <div className="animate-fade-in" style={{ animationDelay: "0.2s" }}>
            <StatCard
              title="Aulas Marcadas"
              value={8}
              subtitle="Para hoje"
              icon={Calendar}
              variant="primary"
              trend={{ value: 12, isPositive: true }}
            />
          </div>
          <div className="animate-fade-in" style={{ animationDelay: "0.3s" }}>
            <StatCard
              title="Alunos Ativos"
              value={24}
              subtitle="Este mês"
              icon={Users}
              variant="accent"
              trend={{ value: 8, isPositive: true }}
            />
          </div>
          <div className="animate-fade-in" style={{ animationDelay: "0.4s" }}>
            <StatCard
              title="Aulas Realizadas"
              value={156}
              subtitle="Este mês"
              icon={CheckCircle}
              variant="success"
              trend={{ value: 15, isPositive: true }}
            />
          </div>
          <div className="animate-fade-in" style={{ animationDelay: "0.5s" }}>
            <StatCard
              title="Horas Trabalhadas"
              value="130h"
              subtitle="Este mês"
              icon={Clock}
              variant="warning"
              trend={{ value: 5, isPositive: true }}
            />
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
          <div className="lg:col-span-2 rounded-2xl border border-border bg-card p-6 shadow-card animate-fade-in" style={{ animationDelay: "0.6s" }}>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-bold text-foreground">Desempenho Semanal</h2>
                <p className="text-sm text-muted-foreground">Aulas realizadas por dia</p>
              </div>
              <TrendingUp className="h-5 w-5 text-success" />
            </div>
            <div className="flex items-end gap-3 h-40">
              {[4, 6, 5, 8, 7, 3, 6].map((value, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-2">
                  <div
                    className="w-full rounded-lg gradient-primary transition-all duration-500 hover:opacity-80"
                    style={{ height: `${(value / 8) * 100}%` }}
                  />
                  <span className="text-xs text-muted-foreground">
                    {["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"][i]}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Lessons Section */}
        <div className="animate-fade-in" style={{ animationDelay: "0.8s" }}>
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-foreground">Próximas Aulas</h2>
              <p className="text-muted-foreground">Suas aulas agendadas para hoje e amanhã</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {mockLessons.map((lesson, i) => (
              <div key={i} className="animate-fade-in" style={{ animationDelay: `${0.9 + i * 0.1}s` }}>
                <LessonCard {...lesson} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Instrutor;
