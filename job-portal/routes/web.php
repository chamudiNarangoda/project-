<?php

use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Admin\DashboardController as AdminDashboardController;
use App\Http\Controllers\Recruiter\DashboardController as RecruiterDashboardController;
use App\Http\Controllers\Seeker\DashboardController as SeekerDashboardController;
use Illuminate\Support\Facades\Auth;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('/redirect-by-role', function () {
    $user = Auth::user();
    if (!$user) {
        return redirect()->route('login');
    }
    return match ($user->role) {
        'admin' => redirect()->route('admin.dashboard'),
        'recruiter' => redirect()->route('recruiter.dashboard'),
        default => redirect()->route('seeker.dashboard'),
    };
})->middleware(['auth', 'verified'])->name('redirect.by.role');

Route::get('/dashboard', function () {
    return view('dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');

    Route::get('/admin', AdminDashboardController::class)->middleware('role:admin')->name('admin.dashboard');
    Route::get('/recruiter', RecruiterDashboardController::class)->middleware('role:recruiter')->name('recruiter.dashboard');
    Route::get('/seeker', SeekerDashboardController::class)->middleware('role:job_seeker')->name('seeker.dashboard');
});

require __DIR__.'/auth.php';
