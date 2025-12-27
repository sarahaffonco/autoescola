import { useState } from "react";
import { Calendar, Clock, Car, User, CheckCircle, MapPin } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

const instructors = [
  { id: 1, name: "Carlos Mendes", speciality: "Categoria A e B", rating: 4.9, available: true },
  { id: 2, name: "Ana Paula", speciality: "Categoria B", rating: 4.8, available: true },
  { id: 3, name: "Roberto Silva", speciality: "Categoria A, B e D", rating: 4.7, available: false },
];

const timeSlots = [
  "08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"
];

const vehicles = [
  { id: 1, type: "Categoria A", description: "Motocicleta", icon: "🏍️" },
  { id: 2, type: "Categoria B", description: "Carro", icon: "🚗" },
  { id: 3, type: "Categoria D", description: "Ônibus", icon: "🚌" },
];

const locations = [
  "Centro - Av. Principal, 123",
  "Zona Sul - Rua das Flores, 456",
  "Zona Norte - Av. Brasil, 789",
];

const Agendamento = () => {
  const [step, setStep] = useState(1);
  const [selectedDate, setSelectedDate] = useState<string>("");
  const [selectedTime, setSelectedTime] = useState<string>("");
  const [selectedInstructor, setSelectedInstructor] = useState<number | null>(null);
  const [selectedVehicle, setSelectedVehicle] = useState<number | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<string>("");

  const handleSubmit = () => {
    toast.success("Aula agendada com sucesso!", {
      description: `Sua aula foi marcada para ${selectedDate} às ${selectedTime}`,
    });
    // Reset form
    setStep(1);
    setSelectedDate("");
    setSelectedTime("");
    setSelectedInstructor(null);
    setSelectedVehicle(null);
    setSelectedLocation("");
  };

  const canProceed = () => {
    switch (step) {
      case 1:
        return selectedDate && selectedTime;
      case 2:
        return selectedInstructor !== null;
      case 3:
        return selectedVehicle !== null && selectedLocation;
      default:
        return false;
    }
  };

  const steps = [
    { number: 1, title: "Data e Hora", icon: Calendar },
    { number: 2, title: "Instrutor", icon: User },
    { number: 3, title: "Veículo e Local", icon: Car },
  ];

  return (
    <div className="min-h-screen bg-background pt-20 pb-12">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-10 animate-fade-in">
          <h1 className="text-3xl font-bold text-foreground mb-2">
            Agendar Aula Prática
          </h1>
          <p className="text-muted-foreground">
            Escolha a data, horário e instrutor para sua próxima aula
          </p>
        </div>

        {/* Progress Steps */}
        <div className="flex items-center justify-center mb-10 animate-fade-in" style={{ animationDelay: "0.1s" }}>
          {steps.map((s, i) => (
            <div key={s.number} className="flex items-center">
              <div
                className={`flex items-center gap-2 px-4 py-2 rounded-full transition-all duration-300 ${
                  step >= s.number
                    ? "gradient-primary text-primary-foreground"
                    : "bg-secondary text-muted-foreground"
                }`}
              >
                <s.icon className="h-4 w-4" />
                <span className="font-medium text-sm hidden sm:inline">{s.title}</span>
              </div>
              {i < steps.length - 1 && (
                <div
                  className={`w-12 h-1 mx-2 rounded-full transition-all duration-300 ${
                    step > s.number ? "gradient-primary" : "bg-secondary"
                  }`}
                />
              )}
            </div>
          ))}
        </div>

        {/* Step Content */}
        <div className="rounded-2xl border border-border bg-card p-8 shadow-card animate-fade-in" style={{ animationDelay: "0.2s" }}>
          {/* Step 1: Date and Time */}
          {step === 1 && (
            <div className="space-y-8">
              <div>
                <h2 className="text-xl font-bold text-foreground mb-4 flex items-center gap-2">
                  <Calendar className="h-5 w-5 text-primary" />
                  Selecione a Data
                </h2>
                <input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  min={new Date().toISOString().split("T")[0]}
                  className="w-full p-4 rounded-xl border border-border bg-background text-foreground focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                />
              </div>

              <div>
                <h2 className="text-xl font-bold text-foreground mb-4 flex items-center gap-2">
                  <Clock className="h-5 w-5 text-primary" />
                  Selecione o Horário
                </h2>
                <div className="grid grid-cols-4 gap-3">
                  {timeSlots.map((time) => (
                    <button
                      key={time}
                      onClick={() => setSelectedTime(time)}
                      className={`p-3 rounded-xl border font-medium transition-all duration-300 ${
                        selectedTime === time
                          ? "gradient-primary text-primary-foreground border-transparent shadow-card"
                          : "border-border bg-secondary/50 text-foreground hover:border-primary"
                      }`}
                    >
                      {time}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Instructor */}
          {step === 2 && (
            <div>
              <h2 className="text-xl font-bold text-foreground mb-6 flex items-center gap-2">
                <User className="h-5 w-5 text-primary" />
                Escolha seu Instrutor
              </h2>
              <div className="space-y-4">
                {instructors.map((instructor) => (
                  <button
                    key={instructor.id}
                    onClick={() => instructor.available && setSelectedInstructor(instructor.id)}
                    disabled={!instructor.available}
                    className={`w-full p-5 rounded-xl border text-left transition-all duration-300 ${
                      selectedInstructor === instructor.id
                        ? "border-primary bg-primary/5 shadow-card"
                        : instructor.available
                        ? "border-border bg-secondary/30 hover:border-primary/50"
                        : "border-border bg-secondary/30 opacity-50 cursor-not-allowed"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="flex h-14 w-14 items-center justify-center rounded-xl gradient-primary text-primary-foreground text-xl font-bold">
                          {instructor.name.charAt(0)}
                        </div>
                        <div>
                          <h3 className="font-semibold text-foreground">{instructor.name}</h3>
                          <p className="text-sm text-muted-foreground">{instructor.speciality}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center gap-1 text-warning">
                          <span>⭐</span>
                          <span className="font-medium text-foreground">{instructor.rating}</span>
                        </div>
                        <span
                          className={`text-xs font-medium ${
                            instructor.available ? "text-success" : "text-destructive"
                          }`}
                        >
                          {instructor.available ? "Disponível" : "Indisponível"}
                        </span>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Step 3: Vehicle and Location */}
          {step === 3 && (
            <div className="space-y-8">
              <div>
                <h2 className="text-xl font-bold text-foreground mb-4 flex items-center gap-2">
                  <Car className="h-5 w-5 text-primary" />
                  Tipo de Veículo
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {vehicles.map((vehicle) => (
                    <button
                      key={vehicle.id}
                      onClick={() => setSelectedVehicle(vehicle.id)}
                      className={`p-5 rounded-xl border text-center transition-all duration-300 ${
                        selectedVehicle === vehicle.id
                          ? "border-primary bg-primary/5 shadow-card"
                          : "border-border bg-secondary/30 hover:border-primary/50"
                      }`}
                    >
                      <span className="text-4xl mb-2 block">{vehicle.icon}</span>
                      <h3 className="font-semibold text-foreground">{vehicle.type}</h3>
                      <p className="text-sm text-muted-foreground">{vehicle.description}</p>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <h2 className="text-xl font-bold text-foreground mb-4 flex items-center gap-2">
                  <MapPin className="h-5 w-5 text-primary" />
                  Local de Encontro
                </h2>
                <div className="space-y-3">
                  {locations.map((location) => (
                    <button
                      key={location}
                      onClick={() => setSelectedLocation(location)}
                      className={`w-full p-4 rounded-xl border text-left transition-all duration-300 ${
                        selectedLocation === location
                          ? "border-primary bg-primary/5 shadow-card"
                          : "border-border bg-secondary/30 hover:border-primary/50"
                      }`}
                    >
                      <span className="text-foreground">{location}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex items-center justify-between mt-8 pt-6 border-t border-border">
            <Button
              variant="outline"
              onClick={() => setStep(step - 1)}
              disabled={step === 1}
              className="px-6"
            >
              Voltar
            </Button>

            {step < 3 ? (
              <Button
                onClick={() => setStep(step + 1)}
                disabled={!canProceed()}
                className="gradient-primary border-0 px-6"
              >
                Continuar
              </Button>
            ) : (
              <Button
                onClick={handleSubmit}
                disabled={!canProceed()}
                className="gradient-primary border-0 px-6"
              >
                <CheckCircle className="h-4 w-4 mr-2" />
                Confirmar Agendamento
              </Button>
            )}
          </div>
        </div>

        {/* Info Card */}
        <div className="mt-8 rounded-2xl border border-border bg-card p-6 shadow-card animate-fade-in" style={{ animationDelay: "0.3s" }}>
          <h3 className="font-semibold text-foreground mb-3">ℹ️ Informações Importantes</h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• Conforme resolução CONTRAN, são obrigatórias 20 horas de aulas práticas</li>
            <li>• Cada aula tem duração de 50 minutos</li>
            <li>• Compareça com 10 minutos de antecedência</li>
            <li>• Traga documento de identificação e comprovante de matrícula</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Agendamento;
