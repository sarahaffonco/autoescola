'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Play, AlertTriangle, CheckCircle2, Clock, User } from 'lucide-react';

export default function AulaPage() {
  const [aulaIniciada, setAulaIniciada] = useState(false);
  const [checklist, setChecklist] = useState({
    documentos: false,
    veiculoRevisado: false,
    cintoSeguranca: false,
    espelhos: false,
    banco: false,
    combustivel: false,
    pneus: false,
    luzes: false,
  });

  const checklistItems = [
    { key: 'documentos', label: 'Documentos do veículo e CNH do instrutor' },
    { key: 'veiculoRevisado', label: 'Verificação geral do veículo (revisão)' },
    { key: 'cintoSeguranca', label: 'Cinto de segurança (aluno e instrutor)' },
    { key: 'espelhos', label: 'Ajuste de espelhos retrovisores' },
    { key: 'banco', label: 'Ajuste de banco e volante' },
    { key: 'combustivel', label: 'Nível de combustível adequado' },
    { key: 'pneus', label: 'Verificação de pneus e calibragem' },
    { key: 'luzes', label: 'Funcionamento de luzes e sinalização' },
  ];

  const dicasSeguranca = [
    'Sempre mantenha distância segura do veículo da frente',
    'Observe constantemente os espelhos retrovisores',
    'Sinalize todas as manobras com antecedência',
    'Respeite os limites de velocidade e sinalizações',
    'Esteja atento a pedestres e ciclistas',
    'Evite distrações durante a condução',
    'Use o freio motor em descidas prolongadas',
    'Mantenha as duas mãos no volante sempre que possível',
  ];

  const todosMarcados = Object.values(checklist).every(item => item);

  const handleChecklistChange = (key: string) => {
    setChecklist(prev => ({
      ...prev,
      [key]: !prev[key as keyof typeof prev]
    }));
  };

  const iniciarAula = () => {
    if (todosMarcados) {
      setAulaIniciada(true);
      // Aqui você pode adicionar lógica para iniciar cronômetro, etc.
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Aula Prática</h1>
            <p className="text-gray-600 mt-1">Prepare e inicie a aula com segurança</p>
          </div>
          <div className="flex items-center gap-4">
            {aulaIniciada && (
              <div className="flex items-center gap-2 text-green-600">
                <Clock className="h-5 w-5" />
                <span className="font-semibold">Aula em andamento</span>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Checklist CONTRAN */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-blue-600" />
                Checklist Pré-Aula (CONTRAN)
              </CardTitle>
              <CardDescription>
                Verifique todos os itens antes de iniciar a aula prática
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {checklistItems.map((item) => (
                <div key={item.key} className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg transition">
                  <Checkbox
                    id={item.key}
                    checked={checklist[item.key as keyof typeof checklist]}
                    onCheckedChange={() => handleChecklistChange(item.key)}
                    disabled={aulaIniciada}
                  />
                  <label
                    htmlFor={item.key}
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer flex-1"
                  >
                    {item.label}
                  </label>
                </div>
              ))}

              {!todosMarcados && !aulaIniciada && (
                <Alert>
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>
                    Complete todos os itens do checklist antes de iniciar a aula
                  </AlertDescription>
                </Alert>
              )}

              <Button
                onClick={iniciarAula}
                disabled={!todosMarcados || aulaIniciada}
                className="w-full mt-4"
                size="lg"
              >
                <Play className="mr-2 h-5 w-5" />
                {aulaIniciada ? 'Aula em Andamento' : 'Iniciar Aula'}
              </Button>
            </CardContent>
          </Card>

          {/* Dicas de Segurança */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-yellow-600" />
                Dicas de Segurança
              </CardTitle>
              <CardDescription>
                Orientações importantes durante a aula
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {dicasSeguranca.map((dica, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm">
                    <span className="text-blue-600 font-bold mt-0.5">•</span>
                    <span className="text-gray-700">{dica}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>

        {/* Informações da Aula */}
        {aulaIniciada && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5 text-blue-600" />
                Informações da Aula
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <p className="text-sm text-gray-600">Aluno</p>
                  <p className="text-lg font-semibold text-gray-900">João Silva</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <p className="text-sm text-gray-600">Categoria</p>
                  <p className="text-lg font-semibold text-gray-900">B</p>
                </div>
                <div className="p-4 bg-yellow-50 rounded-lg">
                  <p className="text-sm text-gray-600">Aula Nº</p>
                  <p className="text-lg font-semibold text-gray-900">5/20</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <p className="text-sm text-gray-600">Veículo</p>
                  <p className="text-lg font-semibold text-gray-900">ABC-1234</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
