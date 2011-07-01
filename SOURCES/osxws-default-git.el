;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;  -*- coding: utf-8-unix -*-
;;  FSF Emacs 23 用 OSXWS git 設定
;;    Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp>
;;    Original Author: IWAI, Masaharu <iwai@alib.jp>
;;      $Id$
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; git の設定
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Git VC backend
(add-to-list 'vc-handled-backends 'GIT t)
(autoload 'git-status "git" "GIT mode." t)
(autoload 'git-blame-mode "git-blame"
 	"Minor mode for incremental blame for Git." t)

(provide 'osxws-default-git)

;; Local Variables:
;; mode: emacs-lisp
;; End:
