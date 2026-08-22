import 'dart:async';

import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:record/record.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(const OdaHudApp());
}

class OdaHudApp extends StatelessWidget {
  const OdaHudApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
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
  late final AnimationController controller;
  WebSocketChannel? socket;
  final AudioRecorder recorder = AudioRecorder();
  final FlutterTts tts = FlutterTts();
  static const MethodChannel voiceChannel = MethodChannel('odas/voice');
  StreamSubscription<Amplitude>? amplitudeSubscription;
  StreamSubscription<Uint8List>? audioSubscription;

  OdaState state = OdaState.idle;
  double audioLevel = 0.0;

  @override
  void initState() {
    super.initState();

    controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 12),
    )..repeat();

    _connectHud();
    _requestPermissions();
  }

  Future<void> _requestPermissions() async {
    final permissions = await [
      Permission.microphone,
      Permission.notification,
    ].request();

    if (permissions[Permission.microphone]?.isGranted == true) {
      await _startMicrophone();
    }
  }

  Future<void> _startMicrophone() async {
    try {
      if (!await recorder.hasPermission()) return;

      final audioStream = await recorder.startStream(
        const RecordConfig(
          encoder: AudioEncoder.pcm16bits,
          sampleRate: 16000,
          numChannels: 1,
        ),
      );

      debugPrint('[MIC] captura iniciada');

        audioSubscription?.cancel();
        audioSubscription = audioStream.listen(
          (Uint8List pcm) {
            try {
              socket?.sink.add(pcm);
              debugPrint('[PCM] enviado: ${pcm.length} bytes');
            } catch (e) {
              debugPrint('[PCM] erro ao enviar: $e');
            }
          },
          onError: (error) {
            debugPrint('[PCM] erro no stream: $error');
          },
        );

      amplitudeSubscription?.cancel();
      amplitudeSubscription = recorder
          .onAmplitudeChanged(const Duration(milliseconds: 80))
          .listen((amplitude) {
        if (!mounted) return;

        final db = amplitude.current;
        final normalized = db.isFinite
            ? ((db + 60.0) / 60.0).clamp(0.0, 1.0)
            : 0.0;

        debugPrint('[MIC] dB=$db level=$normalized');

        setState(() {
          audioLevel = normalized;
        });
      });
    } catch (e) {
      debugPrint('[MIC] erro ao iniciar captura: $e');
    }
  }

  void _connectHud() {
    try {
      socket = WebSocketChannel.connect(
        Uri.parse('ws://192.168.18.4:8766'),
      );

      socket!.stream.listen(
        (message) {
          if (!mounted) return;

          try {
            final data = message.toString();

            final audioMatch = RegExp(
              r'"audio_level"\s*:\s*([0-9.]+)',
            ).firstMatch(data);

            final parsedAudio = audioMatch != null
                ? double.tryParse(audioMatch.group(1)!) ?? 0.0
                : null;

            if (parsedAudio != null) {
              setState(() {
                audioLevel = parsedAudio.clamp(0.0, 1.0);
              });
            }

            if (data.contains('"state":"listening"')) {
              setState(() {
                state = OdaState.listening;
                if (parsedAudio != null) {
                  audioLevel = parsedAudio.clamp(0.0, 1.0);
                }
              });
            } else if (data.contains('"state":"processing"')) {
              setState(() {
                state = OdaState.processing;
                if (parsedAudio != null) {
                  audioLevel = parsedAudio.clamp(0.0, 1.0);
                }
              });
            } else if (data.contains('"state":"idle"')) {
              setState(() {
                state = OdaState.idle;
                audioLevel = 0.0;
              });
            }
          } catch (_) {}
        },
        onError: (_) {},
        onDone: () {},
      );
    } catch (_) {}
  }

  Future<void> speak(String text) async {
    if (text.trim().isEmpty) return;

    try {
      await voiceChannel.invokeMethod('speak', {
        'text': text,
      });
    } catch (e) {
      debugPrint('[TTS] erro: $e');
    }
  }

  @override
  void dispose() {
    amplitudeSubscription?.cancel();
    audioSubscription?.cancel();
    recorder.dispose();
    socket?.sink.close();
    controller.dispose();
    super.dispose();
  }

  void nextState() {
    speak('Olá, eu sou o ODA.');
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

  String get label {
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
      backgroundColor: const Color(0xFF020106),
      body: GestureDetector(
        onTap: nextState,
        child: AnimatedBuilder(
          animation: controller,
          builder: (_, child) {
            return CustomPaint(
              painter: OdaHudPainter(
                progress: controller.value,
                state: state,
                audioLevel: audioLevel,
              ),
              child: SizedBox.expand(
                child: Stack(
                  children: [
                    _topBar(),
                    _centerText(),
                    _bottomPanel(),
                    _sidePanel(),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _topBar() {
    return Positioned(
      top: 28,
      left: 28,
      right: 28,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text(
            'ODA',
            style: TextStyle(
              fontSize: 25,
              fontWeight: FontWeight.w300,
              letterSpacing: 9,
              color: Color(0xFFD7B5FF),
            ),
          ),
          Text(
            label,
            style: const TextStyle(
              fontSize: 11,
              letterSpacing: 4,
              color: Color(0xFFB86CFF),
            ),
          ),
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
      bottom: 145,
      child: Column(
        children: [
          Text(
            label,
            style: const TextStyle(
              fontSize: 13,
              letterSpacing: 7,
              color: Color(0xFFD8B8FF),
            ),
          ),
          const SizedBox(height: 9),
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 220),
            child: Text(
              subtitle,
              key: ValueKey(subtitle),
              style: TextStyle(
                fontSize: 10,
                letterSpacing: 3,
                color: state == OdaState.processing
                    ? const Color(0xFFD6A4FF)
                    : state == OdaState.listening
                        ? const Color(0xFFE7C8FF)
                        : Colors.white38,
              ),
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'TOQUE PARA ALTERAR O ESTADO',
            style: TextStyle(
              fontSize: 7,
              letterSpacing: 2,
              color: Colors.white24,
            ),
          ),
        ],
      ),
    );
  }

  Widget _bottomPanel() {
    return Positioned(
      left: 28,
      right: 28,
      bottom: 25,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const [
          _Metric('CORE', 'ACTIVE'),
          _Metric('STT', '1.55 S'),
          _Metric('RAM', '4.9 GB'),
          _Metric('MODE', 'LOCAL'),
        ],
      ),
    );
  }

  Widget _sidePanel() {
    return Positioned(
      top: 105,
      left: 28,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: const [
          _DataLine('LLM', 'LOCAL'),
          _DataLine('STT', 'WHISPER'),
          _DataLine('VAD', 'ACTIVE'),
          _DataLine('WAKE', 'READY'),
          SizedBox(height: 10),
          _DataLine('CORE', 'ONLINE'),
        ],
      ),
    );
  }
}

class _Metric extends StatelessWidget {
  final String name;
  final String value;

  const _Metric(this.name, this.value);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          name,
          style: const TextStyle(
            fontSize: 7,
            letterSpacing: 2,
            color: Colors.white24,
          ),
        ),
        const SizedBox(height: 3),
        Text(
          value,
          style: const TextStyle(
            fontSize: 10,
            letterSpacing: 1,
            color: Color(0xFFC78CFF),
          ),
        ),
      ],
    );
  }
}

class _DataLine extends StatelessWidget {
  final String name;
  final String value;

  const _DataLine(this.name, this.value);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        children: [
          SizedBox(
            width: 42,
            child: Text(
              name,
              style: const TextStyle(
                fontSize: 7,
                letterSpacing: 1.5,
                color: Colors.white24,
              ),
            ),
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 7,
              letterSpacing: 1.5,
              color: Color(0xFFB96EFF),
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
  final double audioLevel;

  OdaHudPainter({
    required this.progress,
    required this.state,
    required this.audioLevel,
  });

  double get intensity {
    switch (state) {
      case OdaState.idle:
        return 0.55 + audioLevel * 0.15;
      case OdaState.listening:
        return 0.85 + audioLevel * 0.35;
      case OdaState.processing:
        return 1.10 + audioLevel * 0.25;
    }
  }

  double get motion {
    switch (state) {
      case OdaState.idle:
        return 0.22;
      case OdaState.listening:
        return 0.65;
      case OdaState.processing:
        return 1.05;
    }
  }

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(
      size.width / 2,
      size.height / 2 - 35,
    );

    final radius = math.min(size.width, size.height) * 0.31;

    _background(canvas, size);
    _particles(canvas, center, radius);
    _radialStructure(canvas, center, radius);
    _outerHud(canvas, center, radius);
    _orbits(canvas, center, radius);
    _wave(canvas, center, radius);
    _core(canvas, center, radius);

    if (state == OdaState.processing) {
      _avatarFrame(canvas, center, radius);
    }
  }

  void _background(Canvas canvas, Size size) {
    final shader = const RadialGradient(
      colors: [
        Color(0xFF18052B),
        Color(0xFF080311),
        Color(0xFF010106),
      ],
      stops: [0, .45, 1],
    ).createShader(
      Rect.fromCenter(
        center: Offset(size.width / 2, size.height / 2),
        width: size.width,
        height: size.height,
      ),
    );

    canvas.drawRect(
      Offset.zero & size,
      Paint()..shader = shader,
    );

    final grid = Paint()
      ..color = const Color(0xFF29103D)
      ..strokeWidth = .25;

    for (double x = 0; x < size.width; x += 32) {
      canvas.drawLine(
        Offset(x, 0),
        Offset(x, size.height),
        grid,
      );
    }

    for (double y = 0; y < size.height; y += 32) {
      canvas.drawLine(
        Offset(0, y),
        Offset(size.width, y),
        grid,
      );
    }
  }

  void _particles(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    for (int i = 0; i < 110; i++) {
      final angle =
          i * 2.399963 +
          progress * motion * (i.isEven ? .95 : -.70);

      final baseDistance =
          radius * (.58 + ((i * 47) % 100) / 190);

      final audioOffset =
          audioLevel * radius * .055 * math.sin(i * 1.7);

      final distance = baseDistance + audioOffset;

      final x = center.dx + math.cos(angle) * distance;
      final y =
          center.dy + math.sin(angle) * distance * .58;

      final particleSize =
          .45 + ((i * 17) % 6) * .28;

      final alpha =
          (.10 + (i % 5) * .065) * intensity;

      final paint = Paint()
        ..color = const Color(0xFFC77DFF)
            .withValues(alpha: alpha.clamp(0.0, .75));

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
      ..color = const Color(0xFFA64DFF)
          .withValues(alpha: .13 * intensity)
      ..strokeWidth = .55;

    for (int i = 0; i < 48; i++) {
      final angle =
          i * math.pi * 2 / 48 +
          progress * math.pi * 2 * .18;

      final inner = radius * .74;
      final outer =
          radius * (.90 + (i % 4) * .035);

      canvas.drawLine(
        Offset(
          center.dx + math.cos(angle) * inner,
          center.dy + math.sin(angle) * inner * .58,
        ),
        Offset(
          center.dx + math.cos(angle) * outer,
          center.dy + math.sin(angle) * outer * .58,
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
      width: radius * 2.55,
      height: radius * 1.42,
    );

    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = .8
      ..color = const Color(0xFFB35CFF)
          .withValues(alpha: .22 * intensity);

    canvas.drawOval(rect, paint);

    paint
      ..strokeWidth = 1.6
      ..color = const Color(0xFFD09AFF)
          .withValues(alpha: .62);

    final start =
        progress * math.pi * 2 * .35;

    canvas.drawArc(
      rect,
      start,
      math.pi * .38,
      false,
      paint,
    );

    canvas.drawArc(
      rect,
      start + math.pi * 1.18,
      math.pi * .18,
      false,
      paint,
    );

    for (int i = 0; i < 8; i++) {
      final a =
          progress * math.pi * 2 * .12 +
          i * math.pi / 4;

      final p1 = Offset(
        center.dx + math.cos(a) * radius * 1.18,
        center.dy + math.sin(a) * radius * .66,
      );

      final p2 = Offset(
        center.dx + math.cos(a) * radius * 1.25,
        center.dy + math.sin(a) * radius * .70,
      );

      canvas.drawLine(p1, p2, paint);
    }
  }

  void _orbits(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    for (int i = 0; i < 5; i++) {
      final r = radius * (.40 + i * .105);

      final rect = Rect.fromCenter(
        center: center,
        width: r * 2,
        height: r * 1.12,
      );

      final paint = Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = i == 2 ? 1.25 : .55
        ..color = const Color(0xFFB963FF)
            .withValues(
              alpha: (.15 + i * .025) * intensity,
            );

      canvas.save();

      canvas.translate(center.dx, center.dy);

      canvas.rotate(
        progress *
            math.pi *
            2 *
            (i.isEven ? 1 : -1) *
            (0.45 + i * .07),
      );

      canvas.translate(-center.dx, -center.dy);

      canvas.drawOval(rect, paint);

      canvas.restore();

      final nodeAngle =
          progress *
              math.pi *
              2 *
              (i + 1) *
              .45 +
          i * 1.7;

      final nodeX =
          center.dx + math.cos(nodeAngle) * r;

      final nodeY =
          center.dy +
          math.sin(nodeAngle) * r * .56;

      final nodePaint = Paint()
        ..color = const Color(0xFFE0B6FF)
            .withValues(alpha: .72);

      canvas.drawCircle(
        Offset(nodeX, nodeY),
        i == 2 ? 2.5 : 1.7,
        nodePaint,
      );
    }
  }

  void _wave(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final path = Path();
    const points = 220;

    for (int i = 0; i <= points; i++) {
      final t = i / points;
      final angle = t * math.pi * 2;

      final wave =
          math.sin(
            angle * 8 +
                progress * math.pi * 12 * motion,
          ) *
          (1.5 + intensity * 3.0 + audioLevel * 8.0);

      final r = radius * .30 + wave;

      final x =
          center.dx + math.cos(angle) * r;

      final y =
          center.dy +
          math.sin(angle) * r * .56;

      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }

    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth =
          state == OdaState.idle ? 1.0 : 1.35
      ..color = const Color(0xFFD6A4FF)
          .withValues(
            alpha:
                state == OdaState.idle
                    ? .40
                    : .58,
          );

    canvas.drawPath(path, paint);
  }

  void _core(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final baseRadius = radius * .115;

    final subtlePulse =
        math.sin(
          progress *
              math.pi *
              2 *
              motion,
        ) *
        radius *
        .012;

    final r = baseRadius + subtlePulse;

    final glow = Paint()
      ..shader = RadialGradient(
        colors: [
          const Color(0xFFF2DDFF)
              .withValues(alpha: .40),
          const Color(0xFFC45CFF)
              .withValues(alpha: .22),
          const Color(0xFF7B16B2)
              .withValues(alpha: .10),
          Colors.transparent,
        ],
        stops: const [
          0,
          .20,
          .55,
          1,
        ],
      ).createShader(
        Rect.fromCircle(
          center: center,
          radius: r * 4.8,
        ),
      );

    canvas.drawCircle(
      center,
      r * 4.8,
      glow,
    );

    final core = Paint()
      ..shader = const RadialGradient(
        colors: [
          Colors.white,
          Color(0xFFE9C9FF),
          Color(0xFFB13FFF),
          Color(0xFF351047),
        ],
        stops: [
          0,
          .18,
          .55,
          1,
        ],
      ).createShader(
        Rect.fromCircle(
          center: center,
          radius: r,
        ),
      );

    canvas.drawCircle(
      center,
      r,
      core,
    );

    final halo = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = .8
      ..color = const Color(0xFFE9C9FF)
          .withValues(alpha: .60);

    canvas.drawCircle(
      center,
      r * 1.55,
      halo,
    );

    final arc = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0
      ..strokeCap = StrokeCap.round
      ..color = const Color(0xFFC45CFF)
          .withValues(alpha: .65);

    final arcRect = Rect.fromCircle(
      center: center,
      radius: r * 2.05,
    );

    canvas.drawArc(
      arcRect,
      progress * math.pi * 2,
      math.pi * .72,
      false,
      arc,
    );

    canvas.drawArc(
      arcRect,
      progress * math.pi * 2 + math.pi,
      math.pi * .32,
      false,
      arc,
    );
  }

  void _avatarFrame(
    Canvas canvas,
    Offset center,
    double radius,
  ) {
    final rect = Rect.fromCenter(
      center: center,
      width: radius * 1.05,
      height: radius * 1.30,
    );

    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = .45
      ..color = const Color(0xFFD8A8FF)
          .withValues(alpha: .10);

    canvas.drawOval(rect, paint);
  }

  @override
  bool shouldRepaint(
    covariant OdaHudPainter oldDelegate,
  ) {
    return oldDelegate.progress != progress ||
        oldDelegate.state != state ||
        oldDelegate.audioLevel != audioLevel;
  }
}

