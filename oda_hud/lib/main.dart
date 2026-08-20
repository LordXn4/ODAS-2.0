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
      duration: const Duration(seconds: 20),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void changeState(OdaState newState) {
    setState(() {
      state = newState;
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
      backgroundColor: const Color(0xFF020407),
      body: SafeArea(
        child: GestureDetector(
          onTap: () {
            if (state == OdaState.idle) {
              changeState(OdaState.listening);
            } else if (state == OdaState.listening) {
              changeState(OdaState.processing);
            } else {
              changeState(OdaState.idle);
            }
          },
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
                      _buildTopBar(),
                      _buildCenterLabel(),
                      _buildBottomPanel(),
                      _buildSideData(),
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

  Widget _buildTopBar() {
    return Positioned(
      top: 24,
      left: 28,
      right: 28,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text(
            'ODA',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.w300,
              letterSpacing: 8,
              color: Color(0xFF8FEFFF),
            ),
          ),
          Text(
            stateLabel,
            style: const TextStyle(
              fontSize: 12,
              letterSpacing: 4,
              color: Color(0xFF55DFFF),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCenterLabel() {
    return Positioned(
      left: 0,
      right: 0,
      bottom: 145,
      child: Column(
        children: [
          Text(
            stateLabel,
            style: const TextStyle(
              fontSize: 13,
              letterSpacing: 6,
              fontWeight: FontWeight.w300,
              color: Color(0xFF9DEFFF),
            ),
          ),
          const SizedBox(height: 10),
          Text(
            state == OdaState.listening
                ? 'OUVINDO...'
                : state == OdaState.processing
                    ? 'PROCESSANDO'
                    : 'SISTEMA ONLINE',
            style: const TextStyle(
              fontSize: 11,
              letterSpacing: 3,
              color: Colors.white54,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBottomPanel() {
    return Positioned(
      left: 28,
      right: 28,
      bottom: 28,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          _metric('CPU', '12%'),
          _metric('RAM', '4.9 GB'),
          _metric('STT', '1.55 s'),
          _metric('MODE', 'LOCAL'),
        ],
      ),
    );
  }

  Widget _metric(String title, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 8,
            letterSpacing: 2,
            color: Colors.white38,
          ),
        ),
        const SizedBox(height: 3),
        Text(
          value,
          style: const TextStyle(
            fontSize: 11,
            letterSpacing: 1,
            color: Color(0xFF76E8F7),
          ),
        ),
      ],
    );
  }

  Widget _buildSideData() {
    return Positioned(
      top: 110,
      left: 28,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: const [
          _DataLine('LLM', 'LOCAL'),
          _DataLine('STT', 'WHISPER'),
          _DataLine('VAD', 'ACTIVE'),
          _DataLine('WAKE', 'READY'),
        ],
      ),
    );
  }
}

class _DataLine extends StatelessWidget {
  final String title;
  final String value;

  const _DataLine(this.title, this.value);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 9),
      child: Row(
        children: [
          SizedBox(
            width: 42,
            child: Text(
              title,
              style: const TextStyle(
                fontSize: 8,
                letterSpacing: 1.5,
                color: Colors.white30,
              ),
            ),
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 8,
              letterSpacing: 1.5,
              color: Color(0xFF54D9E9),
            ),
          ),
        ],
      ),
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
      size.height / 2 - 25,
    );

    final maxRadius = math.min(size.width, size.height) * 0.34;

    _drawBackground(canvas, size);
    _drawParticles(canvas, center, maxRadius);
    _drawRadialLines(canvas, center, maxRadius);
    _drawOuterHud(canvas, center, maxRadius);
    _drawOrbitRings(canvas, center, maxRadius);
    _drawAudioWave(canvas, center, maxRadius);
    _drawCore(canvas, center, maxRadius);
  }

  void _drawBackground(Canvas canvas, Size size) {
    final paint = Paint()
      ..shader = const RadialGradient(
        colors: [
          Color(0xFF08222A),
          Color(0xFF03080C),
          Color(0xFF010204),
        ],
        stops: [0.0, 0.45, 1.0],
      ).createShader(
        Rect.fromCenter(
          center: Offset(size.width / 2, size.height / 2),
          width: size.width,
          height: size.height,
        ),
      );

    canvas.drawRect(
      Offset.zero & size,
      paint,
    );

    final gridPaint = Paint()
      ..color = const Color(0xFF0B3038)
      ..strokeWidth = 0.35;

    const spacing = 32.0;

    for (double x = 0; x < size.width; x += spacing) {
      canvas.drawLine(
        Offset(x, 0),
        Offset(x, size.height),
        gridPaint,
      );
    }

    for (double y = 0; y < size.height; y += spacing) {
      canvas.drawLine(
        Offset(0, y),
        Offset(size.width, y),
        gridPaint,
      );
    }
  }

  void _drawParticles(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final paint = Paint()
      ..color = const Color(0xFF59E8F7);

    for (int i = 0; i < 70; i++) {
      final angle = i * 2.399963 + progress * 0.4;
      final distance =
          radius * (0.55 + ((i * 37) % 100) / 220);

      final x = center.dx + math.cos(angle) * distance;
      final y = center.dy + math.sin(angle) * distance * 0.58;

      final size = 0.5 + ((i * 13) % 5) * 0.35;

      paint.color = const Color(0xFF5DE9F7).withValues(
        alpha: 0.18 + ((i % 4) * 0.12),
      );

      canvas.drawCircle(
        Offset(x, y),
        size,
        paint,
      );
    }
  }

  void _drawRadialLines(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final paint = Paint()
      ..color = const Color(0xFF25D8E8).withValues(alpha: 0.15)
      ..strokeWidth = 0.7;

    for (int i = 0; i < 36; i++) {
      final angle =
          (math.pi * 2 / 36) * i + progress * math.pi * 2;

      final inner = radius * 0.72;
      final outer = radius * (0.9 + (i % 3) * 0.04);

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

  void _drawOuterHud(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0
      ..color = const Color(0xFF28D8E8).withValues(alpha: 0.35);

    final rect = Rect.fromCenter(
      center: center,
      width: radius * 2.4,
      height: radius * 1.35,
    );

    canvas.drawOval(rect, paint);

    paint
      ..strokeWidth = 2
      ..color = const Color(0xFF5CEBFA).withValues(alpha: 0.7);

    final start =
        progress * math.pi * 2;

    canvas.drawArc(
      rect,
      start,
      math.pi * 0.65,
      false,
      paint,
    );

    canvas.drawArc(
      rect,
      start + math.pi,
      math.pi * 0.3,
      false,
      paint,
    );
  }

  void _drawOrbitRings(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    for (int i = 0; i < 4; i++) {
      final r = radius * (0.48 + i * 0.105);

      final paint = Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = i == 1 ? 1.5 : 0.7
        ..color = const Color(0xFF46E5F5).withValues(alpha: 
          0.22 + intensity * 0.13,
        );

      final rect = Rect.fromCenter(
        center: center,
        width: r * 2,
        height: r * 1.12,
      );

      canvas.save();

      canvas.translate(center.dx, center.dy);
      canvas.rotate(
        progress * (i.isEven ? 1 : -1) * math.pi * 2,
      );
      canvas.translate(-center.dx, -center.dy);

      canvas.drawOval(rect, paint);

      canvas.restore();
    }
  }

  void _drawAudioWave(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2
      ..color = const Color(0xFF63F1FF).withValues(alpha: 0.65);

    final path = Path();

    const points = 160;

    for (int i = 0; i <= points; i++) {
      final normalized = i / points;
      final angle = normalized * math.pi * 2;

      final wave = math.sin(
            angle * 9 +
                progress * math.pi * 12,
          ) *
          (4 + intensity * 8);

      final r = radius * 0.43 + wave;

      final x = center.dx + math.cos(angle) * r;
      final y = center.dy + math.sin(angle) * r * 0.56;

      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }

    canvas.drawPath(path, paint);
  }

  void _drawCore(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final pulse =
        math.sin(progress * math.pi * 2) * 5 * intensity;

    final coreRadius =
        radius * 0.22 + pulse;

    final glow = Paint()
      ..shader = RadialGradient(
        colors: [
          const Color(0xFFB9FBFF).withValues(alpha: 0.95),
          const Color(0xFF35E6F5).withValues(alpha: 0.55),
          const Color(0xFF0A8395).withValues(alpha: 0.18),
          Colors.transparent,
        ],
      ).createShader(
        Rect.fromCircle(
          center: center,
          radius: coreRadius * 2.7,
        ),
      );

    canvas.drawCircle(
      center,
      coreRadius * 2.7,
      glow,
    );

    final corePaint = Paint()
      ..shader = const RadialGradient(
        colors: [
          Colors.white,
          Color(0xFFB6FAFF),
          Color(0xFF23D7EA),
          Color(0xFF06343C),
        ],
        stops: [0.0, 0.18, 0.48, 1.0],
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

    final innerPaint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5
      ..color = Colors.white.withValues(alpha: 0.8);

    canvas.drawCircle(
      center,
      coreRadius * 0.7,
      innerPaint,
    );

    final crossPaint = Paint()
      ..color = const Color(0xFFB9FBFF).withValues(alpha: 0.7)
      ..strokeWidth = 0.7;

    canvas.drawLine(
      Offset(center.dx - coreRadius * 1.35, center.dy),
      Offset(center.dx + coreRadius * 1.35, center.dy),
      crossPaint,
    );

    canvas.drawLine(
      Offset(center.dx, center.dy - coreRadius * 1.35),
      Offset(center.dx, center.dy + coreRadius * 1.35),
      crossPaint,
    );
  }

  @override
  bool shouldRepaint(covariant OdaHudPainter oldDelegate) {
    return oldDelegate.progress != progress ||
        oldDelegate.state != state;
  }
}
