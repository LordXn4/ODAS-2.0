import 'dart:math' as math;
import 'package:flutter/material.dart';

void main() {
  runApp(const OdaHudApp());
}

class OdaHudApp extends StatelessWidget {
  const OdaHudApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(useMaterial3: true),
      home: const OdaHud(),
    );
  }
}

enum OdaState {
  idle,
  listening,
  processing,
}

class OdaHud extends StatefulWidget {
  const OdaHud({super.key});

  @override
  State<OdaHud> createState() => _OdaHudState();
}

class _OdaHudState extends State<OdaHud>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  OdaState state = OdaState.idle;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 18),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void cycleState() {
    setState(() {
      switch (state) {
        case OdaState.idle:
          state = OdaState.listening;
          break;
        case OdaState.listening:
          state = OdaState.processing;
          break;
        case OdaState.processing:
          state = OdaState.idle;
          break;
      }
    });
  }

  String get stateLabel {
    switch (state) {
      case OdaState.idle:
        return 'STANDBY';
      case OdaState.listening:
        return 'LISTENING';
      case OdaState.processing:
        return 'PROCESSING';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF03010A),
      body: SafeArea(
        child: GestureDetector(
          onTap: cycleState,
          child: AnimatedBuilder(
            animation: _controller,
            builder: (context, child) {
              return CustomPaint(
                painter: OdaHudPainter(
                  progress: _controller.value,
                  state: state,
                ),
                child: SizedBox.expand(
                  child: Stack(
                    children: [
                      _topBar(),
                      _leftPanel(),
                      _rightPanel(),
                      _centerText(),
                      _bottomPanel(),
                    ],
                  ),
                ),
              );
            },
          ),
        ),
      ),
    );
  }

  Widget _topBar() {
    return Positioned(
      top: 22,
      left: 25,
      right: 25,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text(
            'ODA',
            style: TextStyle(
              fontSize: 25,
              fontWeight: FontWeight.w300,
              letterSpacing: 9,
              color: Color(0xFFD9B8FF),
            ),
          ),
          Row(
            children: [
              Container(
                width: 7,
                height: 7,
                decoration: const BoxDecoration(
                  shape: BoxShape.circle,
                  color: Color(0xFFB45CFF),
                ),
              ),
              const SizedBox(width: 9),
              Text(
                stateLabel,
                style: const TextStyle(
                  fontSize: 10,
                  letterSpacing: 4,
                  color: Color(0xFFC98CFF),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _leftPanel() {
    return Positioned(
      top: 105,
      left: 25,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: const [
          _HudData('CORE', 'ONLINE'),
          _HudData('LLM', 'LOCAL'),
          _HudData('STT', 'WHISPER'),
          _HudData('VAD', 'ACTIVE'),
          _HudData('WAKE', 'READY'),
        ],
      ),
    );
  }

  Widget _rightPanel() {
    return Positioned(
      top: 105,
      right: 25,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: const [
          _HudData('MODE', 'OFFLINE'),
          _HudData('LINK', 'SECURE'),
          _HudData('VOICE', 'PT-BR'),
          _HudData('GPU', 'AUTO'),
          _HudData('CORE', '01'),
        ],
      ),
    );
  }

  Widget _centerText() {
    final subtitle = switch (state) {
      OdaState.idle => 'SISTEMA ONLINE',
      OdaState.listening => 'OUVINDO...',
      OdaState.processing => 'PROCESSANDO...',
    };

    return Positioned(
      left: 0,
      right: 0,
      bottom: 158,
      child: IgnorePointer(
        child: Column(
          children: [
            Text(
              stateLabel,
              style: const TextStyle(
                fontSize: 13,
                letterSpacing: 7,
                fontWeight: FontWeight.w300,
                color: Color(0xFFE2C7FF),
              ),
            ),
            const SizedBox(height: 8),
            Text(
              subtitle,
              style: const TextStyle(
                fontSize: 9,
                letterSpacing: 3,
                color: Color(0xFF9B72C7),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _bottomPanel() {
    return Positioned(
      left: 25,
      right: 25,
      bottom: 23,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const [
          _Metric('CPU', '12%'),
          _Metric('RAM', '4.9 GB'),
          _Metric('STT', '1.55 s'),
          _Metric('MODE', 'LOCAL'),
        ],
      ),
    );
  }
}

class _HudData extends StatelessWidget {
  final String title;
  final String value;

  const _HudData(this.title, this.value);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        children: [
          SizedBox(
            width: 43,
            child: Text(
              title,
              style: const TextStyle(
                fontSize: 7,
                letterSpacing: 1.5,
                color: Color(0xFF6B547D),
              ),
            ),
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 7,
              letterSpacing: 1.5,
              color: Color(0xFFB86EFF),
            ),
          ),
        ],
      ),
    );
  }
}

class _Metric extends StatelessWidget {
  final String title;
  final String value;

  const _Metric(this.title, this.value);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 7,
            letterSpacing: 2,
            color: Color(0xFF624B72),
          ),
        ),
        const SizedBox(height: 3),
        Text(
          value,
          style: const TextStyle(
            fontSize: 10,
            letterSpacing: 1,
            color: Color(0xFFC889FF),
          ),
        ),
      ],
    );
  }
}

class OdaHudPainter extends CustomPainter {
  final double progress;
  final OdaState state;

  OdaHudPainter({
    required this.progress,
    required this.state,
  });

  double get intensity {
    switch (state) {
      case OdaState.idle:
        return 0.35;
      case OdaState.listening:
        return 0.85;
      case OdaState.processing:
        return 1.0;
    }
  }

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(
      size.width / 2,
      size.height / 2 - 18,
    );

    final radius = math.min(size.width, size.height) * 0.34;

    _background(canvas, size, center);
    _particles(canvas, center, radius);
    _radialStructure(canvas, center, radius);
    _outerHud(canvas, center, radius);
    _orbitRings(canvas, center, radius);
    _satellites(canvas, center, radius);
    _audioWave(canvas, center, radius);
    _core(canvas, center, radius);
  }

  void _background(Canvas canvas, Size size, Offset center) {
    final paint = Paint()
      ..shader = const RadialGradient(
        colors: [
          Color(0xFF24103D),
          Color(0xFF0C0614),
          Color(0xFF020107),
        ],
        stops: [0.0, 0.42, 1.0],
      ).createShader(
        Rect.fromCenter(
          center: center,
          width: size.width * 1.15,
          height: size.height * 1.15,
        ),
      );

    canvas.drawRect(Offset.zero & size, paint);

    final grid = Paint()
      ..color = const Color(0xFF32184A).withValues(alpha: 0.25)
      ..strokeWidth = 0.35;

    const spacing = 32.0;

    for (double x = 0; x < size.width; x += spacing) {
      canvas.drawLine(
        Offset(x, 0),
        Offset(x, size.height),
        grid,
      );
    }

    for (double y = 0; y < size.height; y += spacing) {
      canvas.drawLine(
        Offset(0, y),
        Offset(size.width, y),
        grid,
      );
    }

    final vignette = Paint()
      ..shader = RadialGradient(
        colors: [
          Colors.transparent,
          Colors.black.withValues(alpha: 0.48),
        ],
      ).createShader(
        Rect.fromCircle(
          center: center,
          radius: size.longestSide * 0.72,
        ),
      );

    canvas.drawRect(Offset.zero & size, vignette);
  }

  void _particles(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    for (int i = 0; i < 100; i++) {
      final angle =
          i * 2.399963 + progress * (i.isEven ? 0.45 : -0.25);

      final distance =
          radius * (0.58 + ((i * 37) % 100) / 180);

      final x = center.dx + math.cos(angle) * distance;
      final y =
          center.dy + math.sin(angle) * distance * 0.60;

      final particleSize =
          0.45 + ((i * 13) % 5) * 0.32;

      final alpha =
          0.10 + ((i % 5) * 0.07) + intensity * 0.12;

      final paint = Paint()
        ..color = const Color(0xFFC26BFF)
            .withValues(alpha: alpha.clamp(0.0, 1.0));

      canvas.drawCircle(
        Offset(x, y),
        particleSize,
        paint,
      );
    }
  }

  void _radialStructure(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final paint = Paint()
      ..color = const Color(0xFF9D3CFF)
          .withValues(alpha: 0.15 + intensity * 0.08)
      ..strokeWidth = 0.7;

    for (int i = 0; i < 48; i++) {
      final angle =
          i * math.pi * 2 / 48 + progress * math.pi * 2;

      final inner = radius * 0.73;
      final outer =
          radius * (0.88 + (i % 4) * 0.035);

      canvas.drawLine(
        Offset(
          center.dx + math.cos(angle) * inner,
          center.dy + math.sin(angle) * inner * 0.58,
        ),
        Offset(
          center.dx + math.cos(angle) * outer,
          center.dy + math.sin(angle) * outer * 0.58,
        ),
        paint,
      );
    }
  }

  void _outerHud(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final rect = Rect.fromCenter(
      center: center,
      width: radius * 2.5,
      height: radius * 1.42,
    );

    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 0.9
      ..color = const Color(0xFFAA4FFF)
          .withValues(alpha: 0.32);

    canvas.drawOval(rect, paint);

    paint
      ..strokeWidth = 2.2
      ..color = const Color(0xFFD18AFF)
          .withValues(alpha: 0.78);

    final start = progress * math.pi * 2;

    canvas.drawArc(
      rect,
      start,
      math.pi * 0.52,
      false,
      paint,
    );

    paint
      ..strokeWidth = 1.2
      ..color = const Color(0xFF7B2BFF)
          .withValues(alpha: 0.75);

    canvas.drawArc(
      rect,
      start + math.pi,
      math.pi * 0.34,
      false,
      paint,
    );

    final tickPaint = Paint()
      ..color = const Color(0xFFCB82FF)
          .withValues(alpha: 0.45)
      ..strokeWidth = 1;

    for (int i = 0; i < 24; i++) {
      final a = i * math.pi * 2 / 24;

      final p1 = Offset(
        center.dx + math.cos(a) * radius * 1.14,
        center.dy + math.sin(a) * radius * 0.64,
      );

      final p2 = Offset(
        center.dx + math.cos(a) * radius * 1.19,
        center.dy + math.sin(a) * radius * 0.67,
      );

      canvas.drawLine(p1, p2, tickPaint);
    }
  }

  void _orbitRings(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    for (int i = 0; i < 5; i++) {
      final r = radius * (0.42 + i * 0.105);

      final paint = Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = i == 2 ? 1.5 : 0.65
        ..color = const Color(0xFFB95CFF).withValues(
          alpha: 0.16 + intensity * 0.12,
        );

      final rect = Rect.fromCenter(
        center: center,
        width: r * 2,
        height: r * (0.92 + i * 0.035),
      );

      canvas.save();

      canvas.translate(center.dx, center.dy);

      canvas.rotate(
        progress *
            math.pi *
            2 *
            (i.isEven ? 1 : -1),
      );

      canvas.translate(-center.dx, -center.dy);

      canvas.drawOval(rect, paint);

      canvas.restore();
    }
  }

  void _satellites(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    for (int i = 0; i < 4; i++) {
      final angle =
          progress * math.pi * 2 * (i.isEven ? 1 : -1) +
              i * math.pi / 2;

      final distance = radius * (0.72 + i * 0.035);

      final pos = Offset(
        center.dx + math.cos(angle) * distance,
        center.dy + math.sin(angle) * distance * 0.58,
      );

      final glow = Paint()
        ..shader = RadialGradient(
          colors: [
            const Color(0xFFE5B7FF).withValues(alpha: 0.8),
            const Color(0xFF9C3DFF).withValues(alpha: 0.25),
            Colors.transparent,
          ],
        ).createShader(
          Rect.fromCircle(
            center: pos,
            radius: 16,
          ),
        );

      canvas.drawCircle(pos, 16, glow);

      final dot = Paint()
        ..color = const Color(0xFFE5B7FF);

      canvas.drawCircle(pos, 2.4, dot);
    }
  }

  void _audioWave(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.8
      ..color = const Color(0xFFD18AFF)
          .withValues(alpha: 0.72);

    final path = Path();

    const points = 220;

    for (int i = 0; i <= points; i++) {
      final t = i / points;
      final angle = t * math.pi * 2;

      final wave =
          math.sin(
                angle * 9 +
                    progress * math.pi * 12,
              ) *
              (3 + intensity * 9);

      final secondary =
          math.sin(
                angle * 17 -
                    progress * math.pi * 8,
              ) *
              intensity *
              2;

      final r =
          radius * 0.43 + wave + secondary;

      final x = center.dx + math.cos(angle) * r;
      final y =
          center.dy + math.sin(angle) * r * 0.55;

      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }

    canvas.drawPath(path, paint);
  }

  void _core(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final pulse =
        math.sin(progress * math.pi * 2) *
            (4 + intensity * 8);

    final coreRadius =
        radius * 0.205 + pulse;

    final outerGlow = Paint()
      ..shader = RadialGradient(
        colors: [
          const Color(0xFFE7C7FF)
              .withValues(alpha: 0.95),
          const Color(0xFFB341FF)
              .withValues(alpha: 0.55),
          const Color(0xFF741CFF)
              .withValues(alpha: 0.18),
          Colors.transparent,
        ],
      ).createShader(
        Rect.fromCircle(
          center: center,
          radius: coreRadius * 3.1,
        ),
      );

    canvas.drawCircle(
      center,
      coreRadius * 3.1,
      outerGlow,
    );

    final corePaint = Paint()
      ..shader = const RadialGradient(
        colors: [
          Colors.white,
          Color(0xFFE9CFFF),
          Color(0xFFB64CFF),
          Color(0xFF6E16B7),
          Color(0xFF16052B),
        ],
        stops: [
          0.0,
          0.15,
          0.42,
          0.72,
          1.0,
        ],
      ).createShader(
        Rect.fromCircle(
          center: center,
          radius: coreRadius,
        ),
      );

    canvas.drawCircle(
      center,
      coreRadius,
      corePaint,
    );

    final inner = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.4
      ..color = Colors.white
          .withValues(alpha: 0.85);

    canvas.drawCircle(
      center,
      coreRadius * 0.68,
      inner,
    );

    final cross = Paint()
      ..color = const Color(0xFFE8C8FF)
          .withValues(alpha: 0.68)
      ..strokeWidth = 0.7;

    canvas.drawLine(
      Offset(
        center.dx - coreRadius * 1.45,
        center.dy,
      ),
      Offset(
        center.dx + coreRadius * 1.45,
        center.dy,
      ),
      cross,
    );

    canvas.drawLine(
      Offset(
        center.dx,
        center.dy - coreRadius * 1.45,
      ),
      Offset(
        center.dx,
        center.dy + coreRadius * 1.45,
      ),
      cross,
    );

    final coreDot = Paint()
      ..color = Colors.white;

    canvas.drawCircle(
      center,
      coreRadius * 0.09,
      coreDot,
    );
  }

  @override
  bool shouldRepaint(covariant OdaHudPainter oldDelegate) {
    return oldDelegate.progress != progress ||
        oldDelegate.state != state;
  }
}
