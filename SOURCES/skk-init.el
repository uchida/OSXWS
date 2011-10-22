;;
;; skk-init.el
;;
;; 	for Vine Linux with emacsen-common
;; 	Munehiro Yamamoto <munepi@cg8.so-net.ne.jp>

(defcustom vine-default-skk t
  "A boolean for vine-default-skk"
  :type 'boolean)

(add-hook 'vine-default-setup-hook
	  (lambda()
	    (if vine-default-skk
		(require 'vine-default-skk))))

;;; end of file
