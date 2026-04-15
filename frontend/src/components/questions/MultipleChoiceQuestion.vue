<template>
  <div class="flex flex-col flex-1 h-full gap-4">

    <!-- Question title -->
    <div>
      <p class="text-sm text-gray-400">
        Question {{ index + 1 }} of {{ total }}
      </p>
      <h2 class="text-xl font-semibold text-gray-900">
        {{ question.question }}
      </h2>
    </div>

    <!-- Status -->
    <div class="text-xs px-3 py-2 rounded-lg bg-gray-50 border border-gray-200 text-gray-500">
      {{ selected ? 'Selected: ' + selected : 'Drag one ball into the box to select' }}
    </div>

    <!-- Canvas container (IMPORTANT) -->
    <div class="flex-1">
      <canvas
        ref="canvasRef"
        class="w-full h-full rounded-xl cursor-grab"
        @mousedown="handleDown"
        @mousemove="handleMove"
        @mouseup="handleUp"
        @mouseleave="handleUp"
        @touchstart.prevent="handleTouchStart"
        @touchmove.prevent="handleTouchMove"
        @touchend.prevent="handleUp"
      />
    </div>

    <div v-if="confirmMode" class="flex gap-2 justify-center">
      <button @click="confirmSelection" class="px-4 py-2 bg-green-600 text-white rounded">
        Confirm
      </button>
      <button @click="cancelSelection" class="px-4 py-2 bg-gray-400 text-white rounded">
        Cancel
      </button>
    </div>

    <div v-if="selected" class="flex items-center justify-between px-3 py-2 bg-black text-white rounded-lg">
      <span>Selected: {{ selected }}</span>
      <button @click="resetSelection" class="underline text-sm">Reset</button>
    </div>
    <!-- Button -->
    <button
      @click="submit"
      :disabled="question.required && !selected"
      class="mt-auto px-6 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white disabled:bg-gray-300 disabled:cursor-not-allowed transition"
    >
      Next
    </button>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps<{ question: any; index: number; total: number }>()
const emit = defineEmits<{
  (e: 'answer', payload: { questionId: string; value: string }): void
  (e: 'next'): void
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
let ctx: CanvasRenderingContext2D | null = null
let animId = 0
let W = 0
const H = 320

const BALL_COLORS = [
  '#f87171','#fb923c','#fbbf24','#4ade80','#34d399',
  '#22d3ee','#60a5fa','#818cf8','#c084fc','#f472b6'
]

interface Ball {
  x: number
  y: number
  r: number
  color: string
  label: string
  broken: boolean
  brokenAt: number
}

let balls: Ball[] = []

const selected = ref<string | null>(null)
let lastBroken: Ball | null = null

let hammerPivot = { x: 0, y: 0 }
let angle = 0
const radius = 70
const speed = 0.08
let holding = false

function initBalls() {
  balls = props.question.choices.map((label: string, i: number) => ({
    x: 60 + Math.random() * (W * 0.5 - 80),
    y: 60 + Math.random() * (H - 120),
    r: 26,
    color: BALL_COLORS[i % BALL_COLORS.length],
    label,
    broken: false,
    brokenAt: 0
  }))
  lastBroken = null
}

function resetSelection() {
  selected.value = null
  initBalls()
}

function getPos(e: MouseEvent | Touch) {
  const r = canvasRef.value!.getBoundingClientRect()
  return { x: e.clientX - r.left, y: e.clientY - r.top }
}

function handleDown(e: MouseEvent) {
  holding = true
  hammerPivot = getPos(e)
}

function handleMove(e: MouseEvent) {
  if (holding) hammerPivot = getPos(e)
}

function handleTouchStart(e: TouchEvent) {
  holding = true
  hammerPivot = getPos(e.touches[0])
}

function handleTouchMove(e: TouchEvent) {
  if (holding) hammerPivot = getPos(e.touches[0])
}

function handleUp() {
  holding = false
}

function checkHit(hx: number, hy: number) {
  balls.forEach(b => {
    if (!b.broken && Math.hypot(hx - b.x, hy - b.y) < b.r) {
      b.broken = true
      b.brokenAt = Date.now()
      selected.value = b.label
      lastBroken = b
    }
  })
}

function drawHammer(hx: number, hy: number) {
  if (!ctx) return

  const dx = hx - hammerPivot.x
  const dy = hy - hammerPivot.y
  const ang = Math.atan2(dy, dx)

  ctx.save()
  ctx.translate(hammerPivot.x, hammerPivot.y)
  ctx.rotate(ang)

  ctx.fillStyle = '#92400e'
  ctx.fillRect(0, -3, radius, 6)

  ctx.fillStyle = '#374151'
  ctx.fillRect(radius - 5, -10, 20, 20)

  ctx.restore()
}

function drawBrokenBubble(b: Ball) {
  if (!ctx) return

  ctx.save()
  ctx.strokeStyle = b.color
  ctx.lineWidth = 2

  for (let i = 0; i < 6; i++) {
    const a = (Math.PI * 2 * i) / 6
    ctx.beginPath()
    ctx.moveTo(b.x, b.y)
    ctx.lineTo(b.x + Math.cos(a) * b.r, b.y + Math.sin(a) * b.r)
    ctx.stroke()
  }

  ctx.restore()
}

function loop() {
  if (!ctx) return
  ctx.clearRect(0, 0, W, H)

  ctx.fillStyle = '#f8fafc'
  ctx.fillRect(0, 0, W, H)

  balls.forEach(b => {
    if (b.broken) return

    ctx!.fillStyle = b.color
    ctx!.beginPath()
    ctx!.arc(b.x, b.y, b.r, 0, Math.PI * 2)
    ctx!.fill()

    ctx!.fillStyle = '#fff'
    ctx!.font = 'bold 10px sans-serif'
    ctx!.textAlign = 'center'
    ctx!.textBaseline = 'middle'
    ctx!.fillText(b.label, b.x, b.y)
  })

  if (lastBroken) drawBrokenBubble(lastBroken)

  if (holding) {
    angle += speed
    const hx = hammerPivot.x + Math.cos(angle) * radius
    const hy = hammerPivot.y + Math.sin(angle) * radius

    checkHit(hx, hy)
    drawHammer(hx, hy)
  }

  animId = requestAnimationFrame(loop)
}

function submit() {
  emit('answer', { questionId: props.question._id, value: selected.value ?? '' })
  emit('next')
}

onMounted(() => {
  const canvas = canvasRef.value!
  W = canvas.parentElement!.offsetWidth
  canvas.width = W
  canvas.height = H
  ctx = canvas.getContext('2d')

  initBalls()
  animId = requestAnimationFrame(loop)
})

onUnmounted(() => cancelAnimationFrame(animId))

watch(() => props.question._id, () => {
  selected.value = null
  initBalls()
})
</script>