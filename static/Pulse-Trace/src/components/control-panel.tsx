"use client";

import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FastForward, Palette, Zap } from "lucide-react";
import type { Dispatch, SetStateAction } from "react";

interface ControlPanelProps {
  speed: number;
  setSpeed: Dispatch<SetStateAction<number>>;
  intensity: number;
  setIntensity: Dispatch<SetStateAction<number>>;
  busColor: string;
  setBusColor: Dispatch<SetStateAction<string>>;
  pulseColor: string;
  setPulseColor: Dispatch<SetStateAction<string>>;
}

export function ControlPanel({
  speed,
  setSpeed,
  intensity,
  setIntensity,
  busColor,
  setBusColor,
  pulseColor,
  setPulseColor,
}: ControlPanelProps) {
  return (
    <Card className="w-full border-0 bg-transparent shadow-none">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Zap className="h-5 w-5" />
          Parameters
        </CardTitle>
      </CardHeader>
      <CardContent className="grid gap-8">
        <div className="grid gap-3">
          <Label htmlFor="speed" className="flex items-center gap-2">
            <FastForward className="h-4 w-4" />
            Speed
          </Label>
          <div className="flex items-center gap-4">
            <Slider
              id="speed"
              min={1}
              max={15}
              step={0.5}
              value={[speed]}
              onValueChange={(value) => setSpeed(value[0])}
            />
            <span className="text-sm font-medium w-12 text-right">{speed.toFixed(1)}s</span>
          </div>
        </div>

        <div className="grid gap-3">
          <Label htmlFor="intensity" className="flex items-center gap-2">
            <Zap className="h-4 w-4" />
            Intensity
          </Label>
          <div className="flex items-center gap-4">
            <Slider
              id="intensity"
              min={1}
              max={20}
              step={1}
              value={[intensity]}
              onValueChange={(value) => setIntensity(value[0])}
            />
             <span className="text-sm font-medium w-12 text-right">{intensity}px</span>
          </div>
        </div>

        <div className="grid gap-3">
          <Label htmlFor="busColor" className="flex items-center gap-2">
            <Palette className="h-4 w-4" />
            Bus Line Color
          </Label>
          <Input
            id="busColor"
            type="color"
            value={busColor}
            onChange={(e) => setBusColor(e.target.value)}
            className="p-1 h-10 w-full cursor-pointer"
          />
        </div>

        <div className="grid gap-3">
          <Label htmlFor="pulseColor" className="flex items-center gap-2">
            <Palette className="h-4 w-4" />
            Pulse Energy Color
          </Label>
          <Input
            id="pulseColor"
            type="color"
            value={pulseColor}
            onChange={(e) => setPulseColor(e.target.value)}
            className="p-1 h-10 w-full cursor-pointer"
          />
        </div>
      </CardContent>
    </Card>
  );
}
