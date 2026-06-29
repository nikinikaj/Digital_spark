<?php
header('Content-Type: text/html; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.html');
    exit;
}

function safeInput($value) {
    return htmlspecialchars(trim((string) $value), ENT_QUOTES, 'UTF-8');
}

$name = safeInput($_POST['name'] ?? '');
$email = safeInput($_POST['email'] ?? '');
$phone = safeInput($_POST['phone'] ?? '');
$message = safeInput($_POST['message'] ?? '');
$budgetAmount = safeInput($_POST['budget_amount'] ?? '');
$budgetPackage = safeInput($_POST['budget_package'] ?? '');
$selectedFeatures = safeInput($_POST['selected_features'] ?? '');
$paymentStatus = safeInput($_POST['payment_status'] ?? 'pending');
$clientSentAt = safeInput($_POST['client_sent_at'] ?? '');
$submittedAt = (new DateTime('now', new DateTimeZone('Europe/Skopje')))->format('Y-m-d H:i:s');

$dbPath = __DIR__ . '/data/submissions.sqlite';
$dbDir = dirname($dbPath);

if (!is_dir($dbDir)) {
    mkdir($dbDir, 0755, true);
}

$error = null;
$success = false;

try {
    $db = new PDO('sqlite:' . $dbPath);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Load and execute schema.sql to ensure table exists
    $schemaFile = __DIR__ . '/schema.sql';
    if (file_exists($schemaFile)) {
        $schema = file_get_contents($schemaFile);
        // Extract only SQLite statements (skip MySQL comments)
        $sqlitePart = preg_replace('/--.*$/m', '', $schema);
        $sqlitePart = preg_replace('/\/\*.*?\*\//s', '', $sqlitePart);
        if (!empty(trim($sqlitePart))) {
            $db->exec($sqlitePart);
        }
    }

    $stmt = $db->prepare(
        'INSERT INTO submissions (name, email, phone, message, budget_amount, budget_package, selected_features, payment_status, client_sent_at, submitted_at)
         VALUES (:name, :email, :phone, :message, :budget_amount, :budget_package, :selected_features, :payment_status, :client_sent_at, :submitted_at)'
    );

    $stmt->execute([
        ':name' => $name,
        ':email' => $email,
        ':phone' => $phone,
        ':message' => $message,
        ':budget_amount' => $budgetAmount,
        ':budget_package' => $budgetPackage,
        ':selected_features' => $selectedFeatures,
        ':payment_status' => $paymentStatus,
        ':client_sent_at' => $clientSentAt,
        ':submitted_at' => $submittedAt,
    ]);
    $success = true;
} catch (Exception $e) {
    $error = $e->getMessage();
}
?><!DOCTYPE html>
<html lang="mk">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Форма испратена</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f4f7fb; color: #10263c; margin: 0; padding: 0; }
    .page { max-width: 720px; margin: 40px auto; padding: 24px; background: #ffffff; border-radius: 24px; box-shadow: 0 24px 60px rgba(16,24,40,.08); }
    h1 { margin-bottom: 18px; }
    p { line-height: 1.7; }
    a { color: #2f80ed; text-decoration: none; font-weight: 700; }
    .error { color: #b91c1c; }
    .success { color: #1d4ed8; }
    .details { margin-top: 18px; padding: 18px; border: 1px solid rgba(47,128,237,.18); border-radius: 18px; background: #f8fbff; }
    .details dt { font-weight: 700; }
    .details dd { margin: 4px 0 12px 0; }
  </style>
</head>
<body>
  <div class="page">
    <?php if ($success): ?>
      <h1>Вашите податоци се запишани</h1>
      <p class="success">Формата е успешно испратена и податоците се зачувани во базата.</p>
      <dl class="details">
        <dt>Име</dt><dd><?= $name ?></dd>
        <dt>Е-пошта</dt><dd><?= $email ?></dd>
        <dt>Буџет</dt><dd><?= $budgetAmount ?> €</dd>
        <dt>Пакет</dt><dd><?= $budgetPackage ?></dd>
        <dt>Избрани опции</dt><dd><?= $selectedFeatures ?: 'Нема' ?></dd>
        <dt>Статус на уплата</dt><dd><?= $paymentStatus ?></dd>
        <dt>Испратено на</dt><dd><?= $clientSentAt ?: 'Автоматски додадено' ?></dd>
      </dl>
    <?php else: ?>
      <h1>Грешка при испраќање</h1>
      <p class="error">Се појави проблем при обидот да се зачуваат вашите податоци.</p>
      <?php if ($error): ?>
        <p class="error"><?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8') ?></p>
      <?php endif; ?>
    <?php endif; ?>
    <p><a href="index.html">Назад на почетната страница</a></p>
  </div>
</body>
</html>
