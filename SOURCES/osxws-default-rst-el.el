;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;  -*- coding: utf-8-unix -*-
;;  FSF Emacs 23 用 OSXWS rst-el 設定
;;    Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp>
;;    Original Author: IWAI, Masaharu <iwai@alib.jp>
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; rst-el の設定
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(require 'rst)

(setq auto-mode-alist
       (append '(
                 ("\\.rst$" . rst-mode)
                 ("\\.rest$" . rst-mode)
;;		 ("\\.txt$" . rst-mode)
		 ) auto-mode-alist))

;; rst-modeのときのインデントにタブを使わない
(add-hook 'rst-mode-hook 
	  '(lambda()
	     (setq indent-tabs-mode nil)))

;; 背景色が暗いとき
;(setq frame-background-mode 'dark)

(provide 'osxws-default-rst-el)

;; Local Variables:
;; mode: emacs-lisp
;; End:
