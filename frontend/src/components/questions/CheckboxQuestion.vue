<template>
  <div class="flex flex-col gap-4">
    <div>
      <p class="text-sm text-gray-400">
        Question {{ index + 1 }} of {{ total }}
      </p>
      <h2 class="text-xl font-semibold text-gray-900">
        {{ question.question }}
      </h2>
    </div>

    <div class="text-xs px-3 py-2 rounded-lg bg-gray-50 border border-gray-200 text-gray-500">
      {{ selected.length ? 'Selected: ' + selected.join(', ') : 'Drag balls into the box to select' }}
    </div>

    <canvas
      ref="canvasRef"
      class="w-full rounded-xl cursor-grab"
      height="320"
      @mousedown="handleDown"
      @mousemove="handleMove"
      @mouseup="handleUp"
      @mouseleave="handleUp"
      @touchstart.prevent="handleTouchStart"
      @touchmove.prevent="handleTouchMove"
      @touchend.prevent="handleUp"
    />

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
  (e: 'answer', payload: { questionId: string; value: string[] }): void
  (e: 'next'): void
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
let ctx: CanvasRenderingContext2D | null = null
let animId = 0
let W = 0
let H = 320

const MAX_SPEED = 20
const FRICTION = 0.98
const BOUNCE = 0.9

interface Ball {
  x: number
  y: number
  vx: number
  vy: number
  r: number
  color: string
  label: string
  inBox: boolean
}

const BALL_COLORS = [
  '#f87171','#fb923c','#fbbf24','#4ade80','#34d399',
  '#22d3ee','#60a5fa','#818cf8','#c084fc','#f472b6'
]

let balls: Ball[] = []
let dragging = false
let dragStart = { x: 0, y: 0 }
let dragCurrent = { x: 0, y: 0 }
let selected = ref<string[]>([])
let box = { x: 0, y: 0, w: 0, h: 0 }

function initBalls() {
  balls = props.question.choices.map((label, i) => ({
    x: 80 + i * 60,
    y: H / 2,
    vx: 0,
    vy: 0,
    r: 22,
    color: BALL_COLORS[i % BALL_COLORS.length],
    label,
    inBox: false
  }))
}

function clampVelocity(b: Ball) {
  const speed = Math.hypot(b.vx, b.vy)
  if (speed > MAX_SPEED) {
    b.vx = (b.vx / speed) * MAX_SPEED
    b.vy = (b.vy / speed) * MAX_SPEED
  }
}

function updatePhysics() {
  balls.forEach(b => {
    b.x += b.vx
    b.y += b.vy

    b.vx *= FRICTION
    b.vy *= FRICTION

    if (Math.abs(b.vx) < 0.05) b.vx = 0
    if (Math.abs(b.vy) < 0.05) b.vy = 0

    // wall collision
    if (b.x - b.r < 0 || b.x + b.r > W) {
      b.vx *= -BOUNCE
      b.x = Math.max(b.r, Math.min(W - b.r, b.x))
    }
    if (b.y - b.r < 0 || b.y + b.r > H) {
      b.vy *= -BOUNCE
      b.y = Math.max(b.r, Math.min(H - b.r, b.y))
    }

    clampVelocity(b)
  })

  // ball collision
  for (let i = 0; i < balls.length; i++) {
    for (let j = i + 1; j < balls.length; j++) {
      const a = balls[i]
      const b = balls[j]

      const dx = b.x - a.x
      const dy = b.y - a.y
      const dist = Math.hypot(dx, dy)
      const minDist = a.r + b.r

      if (dist < minDist) {
        const nx = dx / dist
        const ny = dy / dist

        const overlap = minDist - dist
        a.x -= nx * overlap / 2
        b.x += nx * overlap / 2
        a.y -= ny * overlap / 2
        b.y += ny * overlap / 2

        const dvx = b.vx - a.vx
        const dvy = b.vy - a.vy
        const impact = dvx * nx + dvy * ny

        if (impact > 0) continue

        const impulse = impact
        a.vx += nx * impulse
        a.vy += ny * impulse
        b.vx -= nx * impulse
        b.vy -= ny * impulse
      }
    }
  }

  // check selection
  balls.forEach(b => {
    b.inBox =
      b.x > box.x &&
      b.x < box.x + box.w &&
      b.y > box.y &&
      b.y < box.y + box.h
  })

  selected.value = balls.filter(b => b.inBox).map(b => b.label)
}

function draw() {
  if (!ctx) return

  ctx.clearRect(0, 0, W, H)

  // background
  ctx.fillStyle = '#f8fafc'
  ctx.fillRect(0, 0, W, H)

  // box
  ctx.strokeStyle = '#6366f1'
  ctx.strokeRect(box.x, box.y, box.w, box.h)

  // balls
  balls.forEach(b => {
    ctx!.beginPath()
    ctx!.arc(b.x, b.y, b.r, 0, Math.PI * 2)
    ctx!.fillStyle = b.color
    ctx!.fill()

    ctx!.fillStyle = '#fff'
    ctx!.font = '10px sans-serif'
    ctx!.textAlign = 'center'
    ctx!.textBaseline = 'middle'
    ctx!.fillText(b.label, b.x, b.y)
  })

  // aiming line
  if (dragging) {
    ctx.strokeStyle = '#000'
    ctx.beginPath()
    ctx.moveTo(dragStart.x, dragStart.y)
    ctx.lineTo(dragCurrent.x, dragCurrent.y)
    ctx.stroke()
  }
}

function loop() {
  updatePhysics()
  draw()
  animId = requestAnimationFrame(loop)
}

function getPos(e: MouseEvent | Touch) {
  const rect = canvasRef.value!.getBoundingClientRect()
  return {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  }
}

function handleDown(e: MouseEvent) {
  dragging = true
  dragStart = getPos(e)
  dragCurrent = dragStart
}

function handleMove(e: MouseEvent) {
  if (!dragging) return
  dragCurrent = getPos(e)
}

function handleUp() {
  if (!dragging) return

  const dx = dragStart.x - dragCurrent.x
  const dy = dragStart.y - dragCurrent.y

  // hit nearest ball
  let closest: Ball | null = null
  let minDist = Infinity

  balls.forEach(b => {
    const d = Math.hypot(b.x - dragStart.x, b.y - dragStart.y)
    if (d < minDist) {
      minDist = d
      closest = b
    }
  })

  if (closest) {
    closest.vx += dx * 0.2
    closest.vy += dy * 0.2
    clampVelocity(closest)
  }

  dragging = false
}

function submit() {
  emit('answer', { questionId: props.question._id, value: selected.value })
  emit('next')
}

onMounted(() => {
  const canvas = canvasRef.value!
  W = canvas.parentElement!.offsetWidth
  canvas.width = W
  canvas.height = H

  ctx = canvas.getContext('2d')

  box = { x: W * 0.6, y: 40, w: W * 0.35, h: H - 80 }

  initBalls()
  loop()
})

onUnmounted(() => cancelAnimationFrame(animId))

watch(() => props.question._id, () => {
  selected.value = []
  initBalls()
})
</script>