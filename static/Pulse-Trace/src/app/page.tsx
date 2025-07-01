"use client";

import React, { useState } from "react";
import { ChipAnimation } from "@/components/chip-animation";
import { ControlPanel } from "@/components/control-panel";
import {
  SidebarProvider,
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarInset,
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";
import { Cpu } from "lucide-react";

// Tipagem explícita das props
interface SidebarMessageHandlerProps {
  setSpeed: React.Dispatch<React.SetStateAction<number>>;
  setIntensity: React.Dispatch<React.SetStateAction<number>>;
  setBusColor: React.Dispatch<React.SetStateAction<string>>;
  setPulseColor: React.Dispatch<React.SetStateAction<string>>;
}

function SidebarMessageHandler({ setSpeed, setIntensity, setBusColor, setPulseColor }: SidebarMessageHandlerProps) {
  const { setOpen } = useSidebar();
  React.useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data === "toggle-config") setOpen(true);
      if (event.data && event.data.type === "pulse-config") {
        if (typeof event.data.speed === "number") setSpeed(event.data.speed);
        if (typeof event.data.intensity === "number") setIntensity(event.data.intensity);
        if (typeof event.data.busColor === "string") setBusColor(event.data.busColor);
        if (typeof event.data.pulseColor === "string") setPulseColor(event.data.pulseColor);
      }
    };
    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, [setOpen, setSpeed, setIntensity, setBusColor, setPulseColor]);
  return null;
}

export default function Home() {
  const [speed, setSpeed] = useState(5); // in seconds
  const [intensity, setIntensity] = useState(8); // in pixels
  const [busColor, setBusColor] = useState("#a0a0a0");
  const [pulseColor, setPulseColor] = useState("#FFD700");
  const [showIntro, setShowIntro] = useState(true); // NOVO: controla tela inicial
  const [fadeOut, setFadeOut] = useState(false); // NOVO: controla fade

  const dynamicStyles = {
    "--speed": `${speed}s`,
    "--intensity": `${intensity}px`,
    "--bus-color": busColor,
    "--pulse-color": pulseColor,
  } as React.CSSProperties;

  // Função para iniciar transição
  function handleEnter() {
    setFadeOut(true);
    setTimeout(() => {
      setShowIntro(false);
    }, 800); // Duração do fade
  }

  return (
    <div className="relative w-full h-screen">
      {/* TELA INICIAL */}
      {showIntro && (
        <div
          className={`fixed inset-0 z-[100] flex flex-col items-center justify-center bg-[#141a1f] transition-opacity duration-700 ${fadeOut ? "opacity-0 pointer-events-none" : "opacity-100"}`}
          style={{ minHeight: "100vh" }}
        >
          <div className="w-full h-full flex items-center justify-center">
            <div className="w-[600px] h-[450px] max-w-full max-h-[80vh]">
              <ChipAnimation />
            </div>
          </div>
          <button
            onClick={handleEnter}
            className="mt-10 px-8 py-4 bg-emerald-500 hover:bg-emerald-600 text-white text-xl font-bold rounded-xl shadow-lg transition-all"
          >
            Entrar
          </button>
        </div>
      )}
      {/* FUNDO ANIMADO: Pulse-Trace */}
      <div className="fixed inset-0 z-0 w-full h-full pointer-events-none select-none">
        <ChipAnimation />
      </div>
      {/* PAINEL PRINCIPAL SOBRE O FUNDO ANIMADO */}
      <SidebarProvider>
        <SidebarMessageHandler
          setSpeed={setSpeed}
          setIntensity={setIntensity}
          setBusColor={setBusColor}
          setPulseColor={setPulseColor}
        />
        <div className={`relative z-10 transition-opacity duration-700 ${showIntro && !fadeOut ? "opacity-0 pointer-events-none" : "opacity-100"}`}>
          <Sidebar>
            <SidebarHeader className="p-0">
              <div className="flex items-center gap-2 p-4">
                <Cpu className="h-8 w-8 text-primary" />
                <h1 className="text-xl font-bold font-headline">Archon</h1>
              </div>
            </SidebarHeader>
            <SidebarContent className="p-0">
              <ControlPanel
                speed={speed}
                setSpeed={setSpeed}
                intensity={intensity}
                setIntensity={setIntensity}
                busColor={busColor}
                setBusColor={setBusColor}
                pulseColor={pulseColor}
                setPulseColor={setPulseColor}
              />
            </SidebarContent>
          </Sidebar>
          <SidebarInset>
            <main className="relative w-full h-screen flex items-center justify-center" style={dynamicStyles}>
              <div className="absolute top-4 left-4 z-10 md:hidden">
                <SidebarTrigger />
              </div>
              <div className="relative w-[700px] h-[500px] bg-transparent border border-border rounded-lg shadow-lg overflow-hidden">
                {/* Aqui pode entrar o conteúdo do painel do projeto */}
                {/* <ChipAnimation /> */}
              </div>
            </main>
          </SidebarInset>
        </div>
      </SidebarProvider>
    </div>
  );
}
